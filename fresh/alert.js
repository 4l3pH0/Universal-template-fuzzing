'use strict';

const puppeteer = require('puppeteer');

(async () => {
    if (process.argv.length < 3) {
        console.error("Usage: node detect_alert.js <html_file_path>");
        process.exit(1);
    }

    const pathToFile = process.argv[2];
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/usr/bin/google-chrome',
        args: ['--no-sandbox']
    });

    const page = await browser.newPage();
    let pwned = 'safe_code';

    page.on('dialog', async dialog => {
        pwned = 'pwned_successful';
        await dialog.dismiss();
    });

    try {
        await page.goto('file://' + pathToFile, { waitUntil: 'networkidle2' });
    } catch (error) {
        console.error("Error loading page:", error);
        await browser.close();
        process.exit(1);
    }

    console.log(pwned);
    await browser.close();
})();
