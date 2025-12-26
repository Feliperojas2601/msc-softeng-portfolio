// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PagePage } from "../../pages/page-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getTestImagePath, hashString } from "../../utils/utils.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

// F002: Crear página
test.describe('Create Page Tests', () => {
    let authPage;
    let navbarPage;
    let pagePage;
    let pageTitle;
    let pageContent;
    let imagePath;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        const testTitle = testInfo.title;
        const testHash = hashString(testTitle);
        const baseSeed = process.env.FAKER_SEED ? Number.parseInt(process.env.FAKER_SEED) : 42;
        const uniqueSeed = baseSeed + testHash;
        faker.seed(uniqueSeed);
        screenshotManager = new ScreenshotManager(page, testInfo);
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        pagePage = new PagePage(page, screenshotManager);
        pageTitle = faker.lorem.sentence();
        pageContent = faker.lorem.paragraphs();
        imagePath = getTestImagePath();
        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);
    });

    // E006: Crear página básica con éxito
    test('Create basic page successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPages();
        await pagePage.clickOnNewPage();
        await pagePage.setPageTitle(pageTitle);
        await pagePage.setPageContent(pageContent);
        await pagePage.clickOnPublishPage();
        await pagePage.clickOnContinueAfterPublish();
        await pagePage.clickOnRightNowPublishPage();
        await pagePage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then 
        const publishedPages = await pagePage.getPublishedPagesTitles();
        expect(publishedPages).toContain(pageTitle);
        await screenshotManager.captureFinalStep();
    });

    // E007: Crear página con imagen principal con éxito
    test('Create page with feature image successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPages();
        await pagePage.clickOnNewPage();
        await pagePage.setPageTitle(pageTitle);
        await pagePage.setPageContent(pageContent);
        await pagePage.setPageFeatureImage(imagePath);
        await pagePage.clickOnPublishPage();
        await pagePage.clickOnContinueAfterPublish();
        await pagePage.clickOnRightNowPublishPage();
        await pagePage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then 
        const publishedPages = await pagePage.getPublishedPagesTitles();
        expect(publishedPages).toContain(pageTitle);
        await screenshotManager.captureFinalStep();
    });
});
