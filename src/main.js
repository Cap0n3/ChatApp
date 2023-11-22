import { homePage } from "./modules/home/homePage";
import { roomPage } from "./modules/room/roomPage";

function initialize() {
    console.log("Sanity check from main.js.");
    const currentPage = window.location.pathname;
    
    if(currentPage === "/chat/") {
        homePage();
    }
    else if(currentPage.match(/^\/chat\/[a-zA-Z0-9_]+\/$/)) {
        roomPage();
    }
    else {
        console.log("Page not found.");
    }
}

window.onload = initialize;