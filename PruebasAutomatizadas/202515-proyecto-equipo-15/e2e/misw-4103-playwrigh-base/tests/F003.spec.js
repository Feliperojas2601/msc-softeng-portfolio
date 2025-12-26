// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { AuthPage } from "../pages/auth-page.js";
import { PostPage } from "../pages/post-page.js";
import { NavbarPage } from "../pages/navbar-page.js";
import { hashString } from "../utils/utils.js";
import { ScreenshotManager } from "../utils/screenshot-manager.js";

// F003: Editar post
test.describe('Create Post Editing Tests', () => {
    
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

        // Page creation per case
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postHeaderContent);
        await postPage.setPostContent(postBodyContent);
        await postPage.setPostFeatureImage();
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);
    });

    // E008: Editar título de publicación
    test('Editing post header', async ({ page }) => {
        
        // Setting new post title
        let postHeaderNewContent = faker.lorem.words(2);
        
        // When
        await postPage.clickOnPostByTitle(postHeaderContent);
        await postPage.setNewPostTitle(postHeaderNewContent);
        await postPage.clickOnUpdate();
        await page.waitForTimeout(2000);
        
        // Then 
        await postPage.clickOnPosts();
        const postRow = await postPage.getPostRowByTitle(postHeaderNewContent);
        await expect(postRow).toBeVisible();
        await screenshotManager.captureFinalStep();
    });
});