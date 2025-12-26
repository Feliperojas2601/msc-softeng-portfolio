// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";
import { getRandomTestImagePath, hashString } from "../../utils/utils.js";

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
        const testTitle = testInfo.title;
        const testHash = hashString(testTitle);
        const baseSeed = process.env.FAKER_SEED ? Number.parseInt(process.env.FAKER_SEED) : 42;
        const uniqueSeed = baseSeed + testHash;
        faker.seed(uniqueSeed);
        screenshotManager = new ScreenshotManager(page, testInfo);
        
        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);

        // Image paths and post content
        postHeaderContent = faker.lorem.words(2);
        postBodyContent = faker.lorem.paragraphs();
        
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