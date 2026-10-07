// Developer-only loopback rehearsal. Never deployed under app/; always forces OFF.
import path from 'node:path';import {fileURLToPath}from'node:url';
process.env.DREAM_AI_ENABLED='false';
const canonical=await import('./server.mjs');
const root=fileURLToPath(new URL('../../app/dream/',import.meta.url));
export function createLabServer(options={}){return canonical.createLabServer({labRoot:root,kitRoot:path.join(root,'kit'),...options});}
export const configuredPort=canonical.configuredPort,startLabServer=canonical.startLabServer;
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){const port=configuredPort();const server=createLabServer();server.on('error',e=>{console.error('Loopback server could not start: '+e.code);process.exitCode=2;});server.listen(port,'127.0.0.1',()=>console.log('Developer Dream rehearsal http://127.0.0.1:'+port+' · live OFF'));}
