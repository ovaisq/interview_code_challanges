const { test, expect } = require('@playwright/test');

test.describe('Timezone Converter Math Validation', () => {
    // Define the IANA Timezone mappings exactly as they appear in the app
    const TIMEZONES = {
        "Pacific": "America/Los_Angeles",
        "India": "Asia/Kolkata",
        "Central": "US/Central",
        "Eastern": "America/New_York"
    };

    /**
     * Helper function to get timezone offset in minutes from UTC.
     * IMPORTANT: Returns offset in format where positive = ahead of UTC, negative = behind UTC
     * Example: India (UTC+5:30) returns +330, Pacific (UTC-8) returns -480
     */
    async function getTimezoneOffset(page, timezoneId) {
        const offsetMinutes = await page.evaluate((tz) => {
            const date = new Date();
            
            // Get UTC time in milliseconds
            const utcTime = date.getTime() + (date.getTimezoneOffset() * 60000);
            
            // Get time in target timezone
            const tzString = date.toLocaleString('en-US', { timeZone: tz });
            const tzDate = new Date(tzString);
            
            // Calculate offset in minutes
            const offset = (tzDate.getTime() - utcTime) / 60000;
            
            return Math.round(offset);
        }, timezoneId);
        
        return offsetMinutes;
    }

    /**
     * Helper to extract HH:MM string from the UI grid.
     * Uses page.evaluate to find the exact element in the DOM.
     */
    async function getGridTime(page, zoneName) {
        // Wait for the conversion grid to be populated
        await page.waitForSelector('#conversionTimeGrid .time-box', { timeout: 10000 });
        
        // Use evaluate to find the exact time in the browser context
        const timeString = await page.evaluate((zone) => {
            const timeBoxes = document.querySelectorAll('#conversionTimeGrid .time-box');
            for (const box of timeBoxes) {
                const label = box.querySelector('label');
                if (label && label.textContent.trim() === zone) {
                    const timeDisplay = box.querySelector('.time-display');
                    return timeDisplay ? timeDisplay.textContent.trim() : null;
                }
            }
            return null;
        }, zoneName);
        
        if (!timeString) {
            throw new Error(`Could not find time for zone: ${zoneName}`);
        }
        
        return timeString;
    }

    /**
     * Convert time from one timezone to another.
     * @param {string} timeStr - Time in HH:MM format
     * @param {number} fromOffset - Source timezone offset in minutes from UTC
     * @param {number} toOffset - Target timezone offset in minutes from UTC
     * @returns {string} Converted time in HH:MM format
     */
    function convertTime(timeStr, fromOffset, toOffset) {
        const [hours, minutes] = timeStr.split(':').map(Number);
        const totalMinutes = hours * 60 + minutes;
        
        // Convert to UTC
        const utcMinutes = totalMinutes - fromOffset;
        
        // Convert to target timezone
        let targetMinutes = utcMinutes + toOffset;
        
        // Normalize to 0-1439 range (handle day boundaries)
        targetMinutes = ((targetMinutes % 1440) + 1440) % 1440;
        
        const targetHours = Math.floor(targetMinutes / 60);
        const targetMins = targetMinutes % 60;
        
        return `${String(targetHours).padStart(2, '0')}:${String(targetMins).padStart(2, '0')}`;
    }

    test('should verify offset between Pacific and Eastern', async ({ page }) => {
        await page.goto('http://localhost:8000/timezone_converter.html');
        await page.waitForLoadState('networkidle');

        // Setup: 10:00 AM, anchored to Pacific
        await page.selectOption('#anchorTimezone', 'Pacific');
        
        const inputTime = '10:00';
        await page.fill('#timeInput', inputTime);
        await page.press('#timeInput', 'Enter');
        await page.waitForTimeout(500);

        // Get displayed times from conversion grid
        const uiPacific = await getGridTime(page, 'Pacific');
        const uiEastern = await getGridTime(page, 'Eastern');

        // Verify Anchor input matches UI
        expect(uiPacific).toBe('10:00');

        // Get timezone offsets
        const pacificOffset = await getTimezoneOffset(page, TIMEZONES['Pacific']);
        const easternOffset = await getTimezoneOffset(page, TIMEZONES['Eastern']);

        // Calculate expected Eastern time
        const expectedEastern = convertTime(uiPacific, pacificOffset, easternOffset);

        console.log(`Pacific: ${uiPacific} (UTC${pacificOffset >= 0 ? '+' : ''}${pacificOffset/60})`);
        console.log(`Eastern: ${uiEastern} (expected: ${expectedEastern}) (UTC${easternOffset >= 0 ? '+' : ''}${easternOffset/60})`);

        // Assertion
        expect(uiEastern).toBe(expectedEastern);
    });

    test('should verify offset between Pacific and India', async ({ page }) => {
        await page.goto('http://localhost:8000/timezone_converter.html');
        await page.waitForLoadState('networkidle');

        // Setup: 14:30, anchored to Pacific
        await page.selectOption('#anchorTimezone', 'Pacific');
        
        const inputTime = '14:30';
        await page.fill('#timeInput', inputTime);
        await page.press('#timeInput', 'Enter');
        await page.waitForTimeout(500);

        const uiPacific = await getGridTime(page, 'Pacific');
        const uiIndia = await getGridTime(page, 'India');

        // Get timezone offsets
        const pacificOffset = await getTimezoneOffset(page, TIMEZONES['Pacific']);
        const indiaOffset = await getTimezoneOffset(page, TIMEZONES['India']);

        // Calculate expected India time
        const expectedIndia = convertTime(uiPacific, pacificOffset, indiaOffset);

        console.log(`Pacific: ${uiPacific} (UTC${pacificOffset >= 0 ? '+' : ''}${pacificOffset/60})`);
        console.log(`India: ${uiIndia} (expected: ${expectedIndia}) (UTC${indiaOffset >= 0 ? '+' : ''}${indiaOffset/60})`);

        expect(uiIndia).toBe(expectedIndia);
    });

    test('should verify India 18:00 converts correctly to Pacific', async ({ page }) => {
        await page.goto('http://localhost:8000/timezone_converter.html');
        await page.waitForLoadState('networkidle');

        // Scenario: 18:00 India Time (6:00 PM India)
        await page.selectOption('#anchorTimezone', 'India');
        await page.fill('#timeInput', '18:00');
        await page.press('#timeInput', 'Enter');
        await page.waitForTimeout(500);

        const uiIndia = await getGridTime(page, 'India');
        const uiPacific = await getGridTime(page, 'Pacific');
        const uiCentral = await getGridTime(page, 'Central');

        // Get timezone offsets
        const indiaOffset = await getTimezoneOffset(page, TIMEZONES['India']);
        const pacificOffset = await getTimezoneOffset(page, TIMEZONES['Pacific']);
        const centralOffset = await getTimezoneOffset(page, TIMEZONES['Central']);

        // Calculate expected times
        const expectedPacific = convertTime(uiIndia, indiaOffset, pacificOffset);
        const expectedCentral = convertTime(uiIndia, indiaOffset, centralOffset);

        console.log(`India: ${uiIndia} (UTC${indiaOffset >= 0 ? '+' : ''}${indiaOffset/60})`);
        console.log(`Pacific: ${uiPacific} (expected: ${expectedPacific}) (UTC${pacificOffset >= 0 ? '+' : ''}${pacificOffset/60})`);
        console.log(`Central: ${uiCentral} (expected: ${expectedCentral}) (UTC${centralOffset >= 0 ? '+' : ''}${centralOffset/60})`);

        // India 18:00 should be Pacific 04:30 (previous day in terms of date, but we only show time)
        expect(uiPacific).toBe(expectedPacific);
        expect(uiCentral).toBe(expectedCentral);
    });

    test('should verify all timezone conversions are mathematically correct', async ({ page }) => {
        await page.goto('http://localhost:8000/timezone_converter.html');
        await page.waitForLoadState('networkidle');

        // Test multiple scenarios
        const testCases = [
            { anchor: 'Pacific', time: '09:00' },
            { anchor: 'Eastern', time: '15:00' },
            { anchor: 'India', time: '12:30' },
            { anchor: 'Central', time: '20:00' }
        ];

        for (const testCase of testCases) {
            await page.selectOption('#anchorTimezone', testCase.anchor);
            await page.fill('#timeInput', testCase.time);
            await page.press('#timeInput', 'Enter');
            await page.waitForTimeout(500);

            // Get all displayed times
            const times = {
                'Pacific': await getGridTime(page, 'Pacific'),
                'India': await getGridTime(page, 'India'),
                'Central': await getGridTime(page, 'Central'),
                'Eastern': await getGridTime(page, 'Eastern')
            };

            // Get all offsets
            const offsets = {
                'Pacific': await getTimezoneOffset(page, TIMEZONES['Pacific']),
                'India': await getTimezoneOffset(page, TIMEZONES['India']),
                'Central': await getTimezoneOffset(page, TIMEZONES['Central']),
                'Eastern': await getTimezoneOffset(page, TIMEZONES['Eastern'])
            };

            // Verify anchor time is correct
            expect(times[testCase.anchor]).toBe(testCase.time);

            // Verify all other conversions
            const anchorOffset = offsets[testCase.anchor];
            
            for (const [zone, displayedTime] of Object.entries(times)) {
                if (zone === testCase.anchor) continue;
                
                const expectedTime = convertTime(testCase.time, anchorOffset, offsets[zone]);
                
                console.log(`[${testCase.anchor} ${testCase.time}] ${zone}: ${displayedTime} (expected: ${expectedTime})`);
                expect(displayedTime).toBe(expectedTime);
            }
        }
    });
});
