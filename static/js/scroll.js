window.onload = function () {
    if(window.location.hash === '#postFooter') {
        let postFooter = document.querySelector('#postFooter');
        postFooter.scrollIntoView();
    } else if (window.location.hash.includes('#comment')) {
        let commentLike = document.querySelector(window.location.hash);
        commentLike.scrollIntoView();
    }
}
