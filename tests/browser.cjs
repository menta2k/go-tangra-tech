const moduleRoot = process.env.TANGRA_BROWSER_MODULE_ROOT;
const browserModule = name => require(moduleRoot ? require('path').join(moduleRoot, name) : name);
const { chromium } = browserModule('playwright');
const { default: AxeBuilder } = browserModule('@axe-core/playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = path.resolve(__dirname, '../dist');
const output = fs.mkdtempSync(path.join(require('os').tmpdir(), 'tangra-browser-'));
const executablePath = process.env.TANGRA_BROWSER_EXECUTABLE;
(async () => {
 const browser = await chromium.launch({...(executablePath ? { executablePath } : {}),headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const reports = [];
 const mime = {'.html':'text/html','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml','.json':'application/json'};
 async function setup(options) {
  const context = await browser.newContext(options);
  await context.route('https://tangra.test/**', async route => {
   const url = new URL(route.request().url());
   let rel = decodeURIComponent(url.pathname).replace(/^\/docs\//,'');
   if (rel === '') rel = 'index.html';
   const target = path.join(root, rel);
   if (!target.startsWith(root) || !fs.existsSync(target)) return route.fulfill({status:404,contentType:'text/html',body:fs.readFileSync(path.join(root,'404.html'))});
   await route.fulfill({status:200,contentType:mime[path.extname(target)] || 'text/plain',body:fs.readFileSync(target)});
  });
  return context;
 }
 const desktop = await setup({viewport:{width:1440,height:1000}});
 const page = await desktop.newPage();
 const errors=[]; page.on('pageerror',error=>errors.push(error.message));
 for (const route of ['index.html','architecture/index.html','modules/index.html','modules/asset.html','how-to/asterisk/native.html','how-to/scheduler/docker.html','sources/platform/docs/configuration.html','404.html']) {
  await page.goto('https://tangra.test/docs/'+route);
  await page.waitForLoadState('networkidle');
  assert(await page.locator('h1').count() === 1);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth <= window.innerWidth));
  const a11y = await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  reports.push({route,viewport:'desktop',violations:a11y.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))});
 }
 await page.goto('https://tangra.test/docs/index.html');
 await page.screenshot({path:path.join(output, 'desktop.png'),fullPage:true});
 await page.locator('.search-toggle').click();
 await page.locator('#search-input').fill('LCM native');
 await page.waitForFunction(()=>document.querySelectorAll('#search-results a').length>0);
 assert((await page.locator('#search-results').innerText()).includes('without Docker'));
 await page.locator('#search-results a').first().click();
 assert(page.url().endsWith('how-to/lcm/native.html'));
 await page.keyboard.press('Tab');
 await page.locator('body').click({position:{x:1,y:1}});
 await page.keyboard.press('Tab');
 // Reset for reliable skip-link keyboard test.
 await page.goto('https://tangra.test/docs/index.html');
 await page.keyboard.press('Tab');
 assert(await page.locator('.skip-link').evaluate(el=>el===document.activeElement));
 await page.keyboard.press('Enter');
 assert(await page.locator('main').evaluate(el=>el===document.activeElement));
 const mobile = await setup({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const phone = await mobile.newPage();
 for (const route of ['index.html','architecture/index.html','modules/index.html','modules/asset.html','how-to/asterisk/native.html','how-to/scheduler/docker.html','sources/platform/docs/configuration.html']) {
  await phone.goto('https://tangra.test/docs/'+route);
  assert(await phone.evaluate(()=>document.documentElement.scrollWidth <= window.innerWidth));
  const a11y=await new AxeBuilder({page:phone}).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
  reports.push({route,viewport:'mobile',violations:a11y.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))});
 }
 await phone.goto('https://tangra.test/docs/index.html');
 await phone.screenshot({path:path.join(output, 'mobile.png'),fullPage:true});
 await phone.locator('.mobile-menu summary').click();
 await phone.locator('.mobile-menu a').filter({hasText:'Module directory'}).click();
 assert(phone.url().endsWith('/modules/index.html'));
 const nojs = await setup({viewport:{width:390,height:844},javaScriptEnabled:false});
 const plain=await nojs.newPage();
 await plain.goto('https://tangra.test/docs/index.html');
 assert(await plain.locator('h1').isVisible());
 await plain.locator('.mobile-menu summary').click();
 await plain.locator('.mobile-menu a').filter({hasText:'Installation guides'}).click();
 assert(plain.url().endsWith('/how-to/index.html'));
 await plain.getByRole('link',{name:'Native guide',exact:true}).first().click();
 assert(plain.url().endsWith('/how-to/auth/native.html'));
 assert(await plain.locator('pre').count()>0);
 reports.push({keyboardSkip:true,search:true,mobileNavigation:true,noJavaScript:true,pageErrors:errors});
 fs.writeFileSync(path.join(output, 'report.json'),JSON.stringify(reports,null,2));
 console.log(JSON.stringify(reports,null,2));
 console.log('Browser artifacts: '+output);
 assert(!reports.some(r => r.violations && r.violations.length), 'Accessibility violations found; see report');
 assert(errors.length === 0, 'Browser errors found');
 await browser.close();
})().catch(error=>{console.error(error);process.exit(1);});
