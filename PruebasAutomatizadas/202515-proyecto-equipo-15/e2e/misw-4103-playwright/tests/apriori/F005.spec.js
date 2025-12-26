// Imports
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { nextRecord } from "../../utils/data-pool.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getRandomTestImagePath } from "../../utils/utils.js";
import { getAprioriDataPool } from "../../utils/mockaroo-client.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

// Data pool load
const aprioriData = getAprioriDataPool("F005_apriori.json");

// F003: Editar post
test.describe('Deleting Created Post Test', () => {
    
    // Initialize variables
    let authPage;
    let postPage;
    let navbarPage;
    let postBodyContent;
    let postHeaderContent;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        
        // Index choice
        const record = nextRecord('F005', aprioriData);
        
        // Saving test info
        testInfo.dataPool = record;
        
        // Mapping fields to testInfo for reporting
        testInfo.dataPool = { 
            id: record.id, 
            post_title: record.post_title, 
            post_content: record.post_content };
        
        // Screenshot manager
        screenshotManager = new ScreenshotManager(page, testInfo);
        
        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);

        // Image paths and post content
        postHeaderContent = testInfo.dataPool.post_title;
        postBodyContent = testInfo.dataPool.post_content;
        
        // Navigate to page
        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);

    });

    // F005: Eliminar publicación
    test('Removing post', async ({ page }) => {
        
        // Image path
        let imagePath = getRandomTestImagePath();
        
        // Page creation
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postHeaderContent);
        await postPage.setPostContent(postBodyContent);
        await postPage.setPostFeatureImage(imagePath);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then
        const publishedTitles1 = await postPage.getPublishedPostsTitles();
        expect(publishedTitles1).toContain(postHeaderContent);

        // Page deletion
        await postPage.clickOnPostByTitle(postHeaderContent);
        await postPage.clickOnSettingsSideBar();
        await postPage.deletePost();
        await page.waitForTimeout(3000);
        await postPage.deleteConfirmation();
        await page.waitForTimeout(2000);
        
        // Then
        const publishedTitles2 = await postPage.getPublishedPostsTitles();
        expect(publishedTitles2).not.toContain(postHeaderContent);
        await screenshotManager.captureFinalStep();
    });
});