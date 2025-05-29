'use strict';

const puppeteer = require('puppeteer');    
(async() => {    
const browser = await puppeteer.launch({headless: true, executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox']});
const page = await browser.newPage();   
let pwned = 'safe_code';
const readline = require('readline');

function askQuestion(query) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout,
    });

    return new Promise(resolve => rl.question(query, ans => {
        rl.close();
        resolve(ans);
    }))
}


const pathToFile = await askQuestion("type path to file");
// console.log('PathToFile is ' + pathToFile)
page.on('dialog', async dialog => {
    pwned = 'pwned_succesfull';
    // console.log('pwned_succesfull');
    await dialog.dismiss();
	});
await page.goto('file://' + pathToFile);
console.log(pwned);    
await browser.close();    
})();
