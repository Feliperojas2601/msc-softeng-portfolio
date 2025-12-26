// Imports
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PagePage } from "../../pages/page-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getTestImagePath } from "../../utils/utils.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";
import { getDynamicDataFromMockaroo } from "../../utils/mockaroo-client.js";

// F002: Crear página
test.describe('Create Page Tests', () => {
    
    // Initialize variables
    let authPage;
    let navbarPage;
    let pagePage;
    let pageTitle;
    let pageContent;
    let imagePath;
    let screenshotManager;

    // Defining Schema
    const schema = "5b5e0070";

    // Given
    test.beforeEach(async ({ page }, testInfo) => {

        // Dynamic data load
        const [record] = await getDynamicDataFromMockaroo(1, schema);
        
        // Mapping fields to testInfo for reporting
        testInfo.dataPool = { id: record.id, page_title: record.page_title, page_content: record.page_content };
        
        // Screenshot manager
        screenshotManager = new ScreenshotManager(page, testInfo);

        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        pagePage = new PagePage(page, screenshotManager);

        // Page content and image path
        pageTitle = testInfo.dataPool.page_title;
        pageContent = testInfo.dataPool.page_content;

        // Image path
        imagePath = getTestImagePath();

        // Navigate to page
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
