import { sdk } from '@farcaster/miniapp-sdk'

// Initialize the Mini App
async function initMiniApp() {
    try {
        // Wait for the page to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', ready);
        } else {
            ready();
        }
    } catch (error) {
        console.error('Error initializing Mini App:', error);
        // Even if there's an error, try to call ready to prevent infinite loading
        ready();
    }
}

async function ready() {
    try {
        // After your app is fully loaded and ready to display
        await sdk.actions.ready();
        console.log('Mini App is ready and displayed');
    } catch (error) {
        console.error('Error calling sdk.actions.ready():', error);
    }
}

// Initialize the Mini App when the script loads
initMiniApp();

// Export for potential use in other modules
export { initMiniApp, ready };
