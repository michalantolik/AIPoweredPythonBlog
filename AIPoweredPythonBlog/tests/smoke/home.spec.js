const { test, expect } = require('@playwright/test');

const smokePost = {
  title: 'Smoke Test Post',
  slug: 'smoke-test-post',
  excerpt: 'Stable excerpt for browser smoke tests.',
  author: 'smoke_author',
  relatedTitle: 'Smoke Related Post',
};

test.describe('public blog smoke flow', () => {
  test('reader can browse the homepage and open the featured article', async ({ page }) => {
    await page.goto('/');

    await expect(page).toHaveURL(/\/$/);
    await expect(page.locator('body')).toBeVisible();

    const articleLink = page.getByRole('link', { name: smokePost.title }).first();
    await expect(articleLink).toBeVisible();
    await articleLink.click();

    await expect(page).toHaveURL(new RegExp(`/posts/${smokePost.slug}/$`));
    await expect(page.getByRole('heading', { name: smokePost.title })).toBeVisible();
    await expect(page.locator('body')).toContainText(smokePost.excerpt);
  });

  test('reader can browse the archive and open the about page from navigation', async ({ page }) => {
    await page.goto('/posts/');

    await expect(page).toHaveURL(/\/posts\/$/);
    await expect(page.locator('body')).toBeVisible();
    await expect(page.getByRole('link', { name: smokePost.title }).first()).toBeVisible();

    const aboutLink = page.locator('a[href="/about/"]').first();
    await expect(aboutLink).toBeVisible();
    await aboutLink.click();

    await expect(page).toHaveURL(/\/about\/$/);
    await expect(page.locator('body')).toContainText(/about/i);
  });

  test('reader sees related posts on the detail page', async ({ page }) => {
    await page.goto(`/posts/${smokePost.slug}/`);

    await expect(page.getByRole('heading', { name: smokePost.title })).toBeVisible();
    await expect(page.locator('body')).toContainText(/related posts/i);
    await expect(page.getByRole('link', { name: smokePost.relatedTitle }).first()).toBeVisible();
  });

  test('API health check', async ({ request }) => {
    const response = await request.get('/api/posts/');
    expect(response.ok()).toBeTruthy();
    });

});
