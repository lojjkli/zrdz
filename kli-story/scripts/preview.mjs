// Render still frames for review: node scripts/preview.mjs outDir sec1 sec2 ...
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';

const [outDir, ...secs] = process.argv.slice(2);
const browserExecutable = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const chromiumOptions = {gl: 'swangle'};
const browser = await openBrowser('chrome', {browserExecutable, chromiumOptions});
const composition = await selectComposition({serveUrl, id: 'KLI', puppeteerInstance: browser, chromiumOptions});
for (const s of secs) {
	const frame = Math.round(Number(s) * 24);
	const t0 = Date.now();
	await renderStill({composition, serveUrl, frame, output: path.join(outDir, `f_${s}.jpg`), imageFormat: 'jpeg', jpegQuality: 85, puppeteerInstance: browser, chromiumOptions});
	console.log(s, Date.now() - t0, 'ms');
}
await browser.close({silent: true});
