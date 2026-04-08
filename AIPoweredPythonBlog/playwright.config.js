const { defineConfig, devices } = require('@playwright/test');

const PORT = process.env.PLAYWRIGHT_BASE_PORT || '8000';
const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || `http://127.0.0.1:${PORT}`;
const DJANGO_SETTINGS_MODULE = process.env.DJANGO_SETTINGS_MODULE || 'ai_powered_blog.settings.dev';
const DJANGO_SQLITE_NAME = process.env.DJANGO_SQLITE_NAME || 'playwright.sqlite3';
const INTRO_OVERLAY_ENABLED = process.env.INTRO_OVERLAY_ENABLED || '0';
const SHOW_SIDEBAR_ON_HOME_STARTUP = process.env.SHOW_SIDEBAR_ON_HOME_STARTUP || '1';

const isWindows = process.platform === 'win32';

const serverCommand = isWindows
  ? [
      `if exist ai_powered_blog\\${DJANGO_SQLITE_NAME} del ai_powered_blog\\${DJANGO_SQLITE_NAME}`,
      `python ai_powered_blog\\manage.py migrate --noinput`,
      `python ai_powered_blog\\manage.py runserver 127.0.0.1:${PORT}`,
    ].join(' && ')
  : [
      `rm -f "ai_powered_blog/${DJANGO_SQLITE_NAME}"`,
      `python ai_powered_blog/manage.py migrate --noinput`,
      `python ai_powered_blog/manage.py runserver 127.0.0.1:${PORT}`,
    ].join(' && ');

module.exports = defineConfig({
  testDir: './tests/smoke',
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI
    ? [['github'], ['html', { open: 'never' }]]
    : [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: BASE_URL,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: serverCommand,
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    env: {
      ...process.env,
      DJANGO_SETTINGS_MODULE,
      DJANGO_SQLITE_NAME,
      INTRO_OVERLAY_ENABLED,
      SHOW_SIDEBAR_ON_HOME_STARTUP,
    },
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],
});
