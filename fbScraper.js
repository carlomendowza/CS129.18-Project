var text = ''
var posts = [];

// Compare two arrays to see if they have the same content
function arraysEqual(arr1, arr2) {
    if(arr1.length !== arr2.length)
        return false;
    for(var i = arr1.length; i--;) {
        if(arr1[i] !== arr2[i])
            return false;
    }

    return true;
}

function deleteCurrPosts() {
    var posts = document.querySelectorAll('._4-u2._4-u8');
    posts.forEach(post => {
        if (arraysEqual(post.classList, ["_4-u2", "_4-u8"])) {
            post.parentNode.removeChild(post);
        }
    });
}

function getCurrPosts() {
    var posts = document.querySelectorAll('._4-u2._4-u8');
    posts.forEach(post => {
        if (arraysEqual(post.classList, ["_4-u2", "_4-u8"])) {
            post.querySelectorAll('div[data-ad-preview="message"]').forEach(item => {
                text = `${text}\n\n${item.innerText}`;

                console.log('--Start--');
                let before = item.innerText;
                before = before.replace('...\nSee More', '');
                before = before.replace('...\n\nSee More', '');
                
                if(item.querySelectorAll('.text_exposed_show').length!==0) {
                    for(let exposed of item.querySelectorAll('.text_exposed_show')){
                        before += exposed.innerText;
                    }
                }
                console.log(before);
                console.log('--End--');
            });
        }
    });
}

function getNumber() {
    var all = [];
    var posts = document.querySelectorAll('._4-u2._4-u8');
    posts.forEach(post => {
        if (arraysEqual(post.classList, ["_4-u2", "_4-u8"])) {
            post.querySelectorAll('div[data-ad-preview="message"]').forEach(item => {
                text = `${text}\n\n${item.innerText}`;

                let before = item.innerText;
                before = before.replace('...\nSee More', '');
                before = before.replace('...\n\nSee More', '');
                
                if(item.querySelectorAll('.text_exposed_show').length!==0) {
                    for(let exposed of item.querySelectorAll('.text_exposed_show')){
                        before += exposed.innerText;
                    }
                }

                if (before.includes("Continue Reading")) {
                    // Skip
                }
                else {
                    var date = before.split('Submitted:')[1];
                    all.push(before);
    
                    if (date.includes("September 30, 2018 12:00:01 PM +08")) {
                        console.log('MATCH');
                        console.log(all);
                    }
                }

            });
        }
    });
}

// Checks if new posts have loaded
function checkPage() {
    var posts = document.querySelectorAll('._4-u2._4-u8');
    posts.forEach(post => {
        if (arraysEqual(post.classList, ["_4-u2", "_4-u8"])) {
            // getCurrPosts();
            getNumber();
            deleteCurrPosts();
        }
        else {
            window.scrollBy(0, 1000);
        }
    });
}

function eventFire(el, etype){
    if (el.fireEvent) {
      el.fireEvent('on' + etype);
    } else {
      var evObj = document.createEvent('Events');
      evObj.initEvent(etype, true, false);
      el.dispatchEvent(evObj);
    }
}

// checkPage();
setInterval(function() {
    checkPage();
  }, 1000);
