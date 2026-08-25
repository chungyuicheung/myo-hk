import { test, expect } from '@playwright/test';

test.describe('My O! 首頁功能測試', () => {

  test('首頁應該正確載入', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/My O/);
  });

  test('主要區塊應該存在', async ({ page }) => {
    await page.goto('/');

    await expect(page.locator('nav')).toBeVisible();
    await expect(page.locator('.hero-section')).toBeVisible();
    await expect(page.locator('#designs')).toBeVisible();
    await expect(page.locator('#product-overview')).toBeVisible();
    await expect(page.locator('#contact')).toBeVisible();
  });

  test('產品特點應該顯示正確資訊', async ({ page }) => {
    await page.goto('/');

    const features = page.locator('#product-overview ul li');
    await expect(features).toHaveCount(4);
  });

  test('款式選擇區塊應該有選項', async ({ page }) => {
    await page.goto('/');

    const colorOptions = page.locator('.select-option[data-type="color"]');
    await expect(colorOptions).toHaveCount(2);

    const styleOptions = page.locator('.select-option[data-type="style"]');
    await expect(styleOptions).toHaveCount(5);
  });

  test('聯絡方式區塊應該有社交連結', async ({ page }) => {
    await page.goto('/');

    const instagramLink = page.locator('#contact a[href*="instagram"]');
    await expect(instagramLink).toBeVisible();

    const whatsappLink = page.locator('#contact a[href*="whatsapp"]');
    await expect(whatsappLink).toBeVisible();
  });

  test('訂購表單連結應該存在且正確', async ({ page }) => {
    await page.goto('/');

    const formLinks = page.locator('a[href*="docs.google.com/forms/d/e/1FAIpQLScqX5Fq6dA50bSGzbFa14pFJ5RH3FX3PENF-kUPhuBJluCNVA"]');

    // 三個入口：Hero、#contact 卡片、FAQ 行內
    await expect(formLinks).toHaveCount(3);

    // 全部新視窗開啟且帶 noopener
    const count = await formLinks.count();
    for (let i = 0; i < count; i++) {
      await expect(formLinks.nth(i)).toHaveAttribute('target', '_blank');
      await expect(formLinks.nth(i)).toHaveAttribute('rel', /noopener/);
    }

    // Hero：.hero-section 內可見
    await expect(page.locator('.hero-section a[href*="docs.google.com/forms"]')).toBeVisible();

    // #contact：第三張卡片，含文案
    const contactCard = page.locator('#contact .contact-cta-item[href*="docs.google.com/forms"]');
    await expect(contactCard).toBeVisible();
    await expect(contactCard).toContainText('填寫網上訂購表單');

    // #faq：行內連結位於預設摺疊的 <details> 內，斷言存在即可
    await expect(page.locator('#faq a[href*="docs.google.com/forms"]')).toBeAttached();
  });

  test('頁腳應該存在', async ({ page }) => {
    await page.goto('/');

    const footer = page.locator('footer');
    await expect(footer).toBeVisible();

    await expect(footer.locator('a[href="privacy.html"]')).toBeVisible();
    await expect(footer.locator('a[href="terms.html"]')).toBeVisible();
  });

  test('RWD - 平板尺寸', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');

    // 漢堡選單應該隱藏
    const hamburgerBtn = page.locator('#mobile-menu-button');
    await expect(hamburgerBtn).not.toBeVisible();

    // 桌面選單應該可見
    const desktopMenu = page.locator('.desktop-nav-links');
    await expect(desktopMenu).toBeVisible();
  });

  test('RWD - 桌面尺寸', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('/');

    const desktopMenu = page.locator('.desktop-nav-links');
    await expect(desktopMenu).toBeVisible();

    // Sticky Bar 應該隱藏
    const stickyBar = page.locator('#sticky-conversion-bar');
    await expect(stickyBar).not.toBeVisible();
  });
});