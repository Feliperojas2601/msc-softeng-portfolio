// Imports
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { PagePage } from "../../pages/page-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { TagPage } from "../../pages/tag-page.js";
import { getAprioriDataPool } from "../../utils/mockaroo-client.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

const invalidData = getAprioriDataPool("invalid_data_apriori.json");

test.describe('Invalid Data Tests', () => {
    
    let authPage;
    let navbarPage;
    let postPage;
    let pagePage;
    let tagPage;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        screenshotManager = new ScreenshotManager(page, testInfo);
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        pagePage = new PagePage(page, screenshotManager);
        tagPage = new TagPage(page, screenshotManager);
        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);
    });

    // EI001: Crear publicación con título extremadamente largo (>255 caracteres)
    test('EI001: Create post with extremely long title should truncate or handle gracefully', async ({ page }) => {
        const testData = invalidData.find(d => d.scenario === 'EI001');
        
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(testData.post_title);
        await postPage.setPostContent(testData.post_content);
        await page.waitForTimeout(2000);

        // Then - Verify Ghost prevents publishing with long title (button should not be available/enabled)
        const isVisible = await postPage.isPublishButtonVisible();
        const isEnabled = await postPage.isPublishButtonEnabled();
        if (!isVisible) {
            expect(isVisible).toBeFalsy();
        } else {
            expect(isEnabled).toBeFalsy();
        }
        await screenshotManager.captureFinalStep();
    });

    // EI002: Crear página con título extremadamente largo (>255 caracteres)
    test('EI002: Create page with extremely long title should truncate or handle gracefully', async ({ page }) => {
        const testData = invalidData.find(d => d.scenario === 'EI002');
        
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPages();
        await pagePage.clickOnNewPage();
        await pagePage.setPageTitle(testData.page_title);
        await pagePage.setPageContent(testData.page_content);
        await page.waitForTimeout(2000);

        // Then - Verify Ghost prevents publishing with long title (button should not be available/enabled)
        const isVisible = await pagePage.isPublishButtonVisible();
        const isEnabled = await pagePage.isPublishButtonEnabled();
        if (!isVisible) {
            expect(isVisible).toBeFalsy();
        } else {
            expect(isEnabled).toBeFalsy();
        }
        await screenshotManager.captureFinalStep();
    });

    // EI003: Crear tag con nombre extremadamente largo (>191 caracteres)
    test('EI003: Create tag with extremely long name should show error message', async ({ page }) => {
        const testData = invalidData.find(d => d.scenario === 'EI003');
        
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnTags();
        await page.waitForTimeout(1000);
        await tagPage.clickOnNewTag();
        await tagPage.setTagNameAndSlug(testData.tag_name);
        if (testData.tag_description) {
            await tagPage.setTagDescription(testData.tag_description);
        }
        await page.waitForTimeout(2000);

        // Then - Verify Ghost shows error message for long tag name
        const errorMessage = await tagPage.getErrorMessage();
        expect(errorMessage).toBeTruthy();
        expect(errorMessage.trim()).toContain('Tag names cannot be longer than 191 characters');
        await screenshotManager.captureFinalStep();
    });

    // EI004: Crear tag con slug que contiene caracteres reservados
    // SECURITY RISK: Ghost accepts reserved URL characters (/, ?, #, &) in slugs without sanitization.
    // This can lead to: URL injection attacks, broken routing, XSS vulnerabilities via URL parameters,
    // and potential path traversal issues. Slugs should be sanitized to alphanumeric + hyphens only.
    test('EI004: Create tag with reserved characters in slug - SECURITY VULNERABILITY DETECTED', async ({ page }) => {
        const testData = invalidData.find(d => d.scenario === 'EI004');
        
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnTags();
        await page.waitForTimeout(1000);
        await tagPage.clickOnNewTag();
        await tagPage.setTagName(testData.tag_name);
        await tagPage.setTagSlug(testData.tag_slug);
        if (testData.tag_description) {
            await tagPage.setTagDescription(testData.tag_description);
        }
        await page.waitForTimeout(2000);

        // Then - VERIFY THE SECURITY VULNERABILITY: Ghost ACCEPTS reserved characters without sanitization
        const actualSlug = await tagPage.getTagSlugValue();
        expect(actualSlug).toBeTruthy();
        
        // VULNERABILITY CONFIRMATION: Ghost does NOT sanitize these dangerous characters
        expect(actualSlug).toContain('/');  // Path traversal risk
        expect(actualSlug).toContain('?');  // Query injection risk
        expect(actualSlug).toContain('#');  // Fragment injection risk
        
        // Verify the entire malicious slug is preserved
        expect(actualSlug).toBe(testData.tag_slug);
        await screenshotManager.captureFinalStep();
    });

    // EI005: Crear tag con color en formato inválido
    test('EI005: Create tag with invalid hex color format', async ({ page }) => {
        const testData = invalidData.find(d => d.scenario === 'EI005');
        
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnTags();
        await page.waitForTimeout(1000);
        await tagPage.clickOnNewTag();
        await tagPage.setTagName(testData.tag_name);
        await tagPage.setTagSlug(testData.tag_slug);
        await tagPage.setTagColor(testData.tag_color);
        if (testData.tag_description) {
            await tagPage.setTagDescription(testData.tag_description);
        }
        await page.waitForTimeout(2000);

        // Then - Verify Ghost handles invalid color format
        const actualColor = await tagPage.getTagColorValue();
        expect(actualColor).toBeTruthy();
        
        // Check if Ghost shows error message or sanitizes the color
        const errorMessage = await tagPage.getErrorMessage();
        if (errorMessage) {
            // Ghost shows error for invalid color
            expect(errorMessage.trim()).toContain('color');
        } else {
            // Ghost might accept invalid color or sanitize it
            // Check if save button is disabled due to invalid color
            const isEnabled = await tagPage.isSaveButtonEnabled();
            // Document behavior
            console.log(`⚠️  Color validation: ${isEnabled ? 'ACCEPTS invalid color' : 'REJECTS invalid color'}`);
            console.log(`   Invalid color provided: ${testData.tag_color}`);
            console.log(`   Color in field: ${actualColor}`);
        }
        
        await screenshotManager.captureFinalStep();
    });
});
