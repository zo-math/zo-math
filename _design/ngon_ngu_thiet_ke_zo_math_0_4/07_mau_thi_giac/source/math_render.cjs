const fs=require('fs'),path=require('path');const katex=require('./deps.cjs')('katex');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));const out={};let errors=[];
for(const tex of data){try{let s=katex.renderToString(tex,{output:'mathml',throwOnError:true,strict:false,displayMode:false});out[tex]=s.replace(/^<span class="katex">/,'').replace(/<\/span>$/,'');}catch(e){errors.push({tex,error:String(e)})}}
fs.writeFileSync(process.argv[3],JSON.stringify(out));if(errors.length){console.log(errors);process.exit(1)}console.log('LaTeX expressions:',data.length);
