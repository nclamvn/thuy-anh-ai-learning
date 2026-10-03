export function validateCatalog(payload){
 const fail=()=>{throw new Error('Danh mục thư viện không hợp lệ.');};
 if(!payload||payload.schemaVersion!==1||payload.generatedKind!=='ai-draft-local-kit'||!Array.isArray(payload.items)||payload.items.length>500)fail();
 const ids=new Set();for(const item of payload.items){if(!item||typeof item.id!=='string'||ids.has(item.id)||typeof item.title!=='string'||typeof item.description!=='string'||typeof item.category!=='string'||!['draft','operating-guide','source-index'].includes(item.status)||!Array.isArray(item.sourceIds)||item.sourceIds.some(id=>typeof id!=='string')||typeof item.href!=='string'||!/^resources\/[A-Za-z0-9_./-]+$/.test(item.href)||item.href.split('/').some(part=>part==='..'||part==='.'||part==='')||!item.href.startsWith('resources/'))fail();if(item.translations!==undefined){const en=item.translations?.en;if(!en||typeof en.title!=='string'||typeof en.description!=='string'||!['draft','operating-guide','source-index'].includes(en.status)||typeof en.href!=='string'||!/^resources\/en\/[A-Za-z0-9_./-]+$/.test(en.href)||en.href.split('/').some(part=>part==='..'||part==='.'||part===''))fail();}ids.add(item.id);}
 return structuredClone(payload);
}
const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function resolveDocumentLink(raw,baseHref='resources/README.md'){
 try{
  const href=raw.trim();if(!href||/[\u0000-\u0020\\]/.test(href)||href.startsWith('//'))return null;
  if(/^https:\/\//i.test(href)){const url=new URL(href);if(url.protocol!=='https:'||url.username||url.password)return null;return{href:url.href,external:true};}
  if(/^[a-z][a-z0-9+.-]*:/i.test(href)||href.includes('%'))return null;
  const base=new URL(baseHref,'https://local.invalid/');if(base.origin!=='https://local.invalid'||!base.pathname.startsWith('/resources/'))return null;
  const url=new URL(href,base);if(url.origin!==base.origin||!url.pathname.startsWith('/resources/')||url.pathname.split('/').includes('..')||url.search)return null;
  return{href:url.pathname.slice(1)+url.hash,path:url.pathname.slice(1),external:false};
 }catch{return null;}
}
function inlineMarkdown(text,options={},depth=0){
 if(depth>6)return esc(text);
 const pattern=/(`+)([^`]+)\1|\[([^\]\n]+)\]\(([^)\n]+)\)|\*\*([^*\n]+)\*\*|(?<!_)__(?!_)([^_\n]+)__(?!_)|\*([^*\n]+)\*|(?<!_)_(?!_)([^_\n]+)_(?!_)/g;
 let result='',offset=0,match;
 while((match=pattern.exec(text))){result+=esc(text.slice(offset,match.index));
  if(match[1])result+=`<code>${esc(match[2])}</code>`;
  else if(match[3]){const target=resolveDocumentLink(match[4],options.baseHref);const label=inlineMarkdown(match[3],options,depth+1);if(!target)result+=label;else{const item=!target.external?options.catalog?.find(record=>record.href===target.path):null;result+=item?`<a href="#library" data-doc-link="${esc(item.id)}">${label}</a>`:`<a href="${esc(target.href)}" target="_blank" rel="noopener noreferrer">${label}</a>`;}}
  else if(match[5]||match[6])result+=`<strong>${inlineMarkdown(match[5]||match[6],options,depth+1)}</strong>`;
  else result+=`<em>${inlineMarkdown(match[7]||match[8],options,depth+1)}</em>`;
  offset=pattern.lastIndex;
 }
 return result+esc(text.slice(offset));
}
function tableCells(line){return line.trim().replace(/^\|/,'').replace(/\|$/,'').split(/(?<!\\)\|/).map(cell=>cell.trim().replace(/\\\|/g,'|'));}
function isSeparator(line){return /^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);}
export function safeMarkdown(text,options={}){
 const lines=String(text).replace(/\r\n?/g,'\n').split('\n');let html='',index=0;
 const first=lines.findIndex(line=>line.trim());const title=first<0?null:/^#\s+(.+)$/.exec(lines[first]);
 if(options.previewTitle&&title&&title[1].trim().normalize('NFKC').toLocaleLowerCase('vi')===options.previewTitle.trim().normalize('NFKC').toLocaleLowerCase('vi'))index=first+1;
 while(index<lines.length){const line=lines[index];
  if(!line.trim()){index++;continue;}
  if(/^\s*```/.test(line)){const code=[];index++;while(index<lines.length&&!/^\s*```/.test(lines[index]))code.push(lines[index++]);if(index<lines.length)index++;html+=`<pre class="document-code"><code>${esc(code.join('\n'))}</code></pre>`;continue;}
  const heading=/^(#{1,6})\s+(.+)$/.exec(line);if(heading){const level=Math.min(heading[1].length+1,4);html+=`<h${level}>${inlineMarkdown(heading[2],options)}</h${level}>`;index++;continue;}
  if(index+1<lines.length&&line.includes('|')&&isSeparator(lines[index+1])){
   const headings=tableCells(line),align=tableCells(lines[index+1]).map(cell=>cell.startsWith(':')&&cell.endsWith(':')?'center':cell.endsWith(':')?'right':'left');index+=2;const rows=[];while(index<lines.length&&lines[index].trim()&&lines[index].includes('|'))rows.push(tableCells(lines[index++]));html+=`<div class="document-table-wrap"><table><thead><tr>${headings.map((cell,n)=>`<th class="align-${align[n]||'left'}">${inlineMarkdown(cell,options)}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${headings.map((_,n)=>`<td class="align-${align[n]||'left'}">${inlineMarkdown(row[n]??'',options)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;continue;
  }
  if(/^\s*([-*+] |\d+[.)] )/.test(line)){
   const ordered=/^\s*\d+[.)] /.test(line),tag=ordered?'ol':'ul',start=ordered?Number(line.match(/^\s*(\d+)/)[1]):null;html+=`<${tag}${ordered&&start!==1?` start="${start}"`:''}>`;while(index<lines.length&&new RegExp(ordered?'^\\s*\\d+[.)] ':'^\\s*[-*+] ').test(lines[index])){const content=lines[index++].replace(/^\s*(?:[-*+]|\d+[.)])\s+/,'');html+=`<li>${inlineMarkdown(content,options)}</li>`;}html+=`</${tag}>`;continue;
  }
  if(/^\s*>/.test(line)){const quote=[];while(index<lines.length&&/^\s*>/.test(lines[index]))quote.push(lines[index++].replace(/^\s*>\s?/,''));html+=`<blockquote>${inlineMarkdown(quote.join(' '),options)}</blockquote>`;continue;}
  if(/^\s*(?:---+|\*\*\*+)\s*$/.test(line)){html+='<hr>';index++;continue;}
  const paragraph=[line];index++;while(index<lines.length&&lines[index].trim()&&!/^\s*(#{1,6}\s|```|>|[-*+] |\d+[.)] )/.test(lines[index])&&!(index+1<lines.length&&lines[index].includes('|')&&isSeparator(lines[index+1])))paragraph.push(lines[index++]);html+=`<p>${inlineMarkdown(paragraph.join(' '),options)}</p>`;
 }
 return html;
}
export async function fetchCatalog(){const response=await fetch('./resources/catalog.json');if(!response.ok)throw new Error('Chưa đọc được danh mục tài liệu. Chạy compiler thư viện rồi tải lại.');return validateCatalog(await response.json());}
export async function fetchDocument(item){validateCatalog({schemaVersion:1,generatedKind:'ai-draft-local-kit',items:[item]});const response=await fetch(`./${item.href}`);if(!response.ok)throw new Error('Không đọc được tài liệu; giữ nguyên dữ liệu hiện tại.');const text=await response.text();if(text.length>500000)throw new Error('Tài liệu vượt giới hạn preview 500 KB.');return text;}
