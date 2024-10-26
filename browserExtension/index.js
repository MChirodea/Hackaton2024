async function detectFakeReviews() {
    let [tab] = await chrome.tabs.query({ active: true });
    console.log(tab);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: async () => {
            function getDescriptionBody() {
                let description = document.getElementById('description-body');
                return description;
            }

            function getSpecifications() {
                let specifications = document.getElementsByClassName('specifications-body')[0];
                return specifications;
            }

            function getReviewRows() {
                return document.getElementsByClassName('product-review-item');
            }
            let currentLocation = window.location.href;
            let reviewRows = getReviewRows();

            try {
                await fetch('http://localhost:8000/send-ext-data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: currentLocation,
                        description: getDescriptionBody().innerText,
                        specifications: getSpecifications().innerText
                    }),
                })
            } catch (error) {
                console.error(error);
            }

            // loop through all elements
            for (let reviewRow of reviewRows) {
                // create a random value between 1 and 100
                let random = Math.floor(Math.random() * 100);

                reviewRow.style.backgroundColor = random <= 30 ? '#DF221414' : random > 31 && random < 70 ? '#FBC02D14' : '#1B870014';

                const badgeColor = random <= 30 ? '#DF2214' : random > 31 && random < 70 ? '#FBC02D' : '#1B8700';
                const clickedBadgeColor = random <= 30 ? '#B21B10' : random > 31 && random < 70 ? '#E2AD29' : '#187A00';

                let badgeWrapper = document.createElement('div');
                badgeWrapper.style.display = 'inline-block';
                badgeWrapper.style.marginLeft = '24px';
                badgeWrapper.innerHTML =`<p class="badge">
                                        ${random}% Trustworthy
                                    </p>

                                    <style>
                                        .badge {
                                            border-radius: 40px;
                                            height: 32px;
                                            padding: 8.5px 20px;
                                            width: max-content;
                                            display: flex;
                                            align-items: center;
                                            cursor: pointer;
                                        }
                                        .badge-clicked {
                                            background: "purple";
                                        }
                                    </style>`;
                                    
                reviewRow.getElementsByClassName('star-rating-container')[0].appendChild(badgeWrapper);
                let badge = badgeWrapper.getElementsByClassName('badge')[0];
                badge.style.backgroundColor = badgeColor;
                badge.style.color= random > 31 && random < 70 ? '#000' : '#fff';
                let badgeClicked = false;
                badge.addEventListener('click', () => {
                    if (badgeClicked) {
                        let popup = badgeWrapper.getElementsByClassName('popup')[0];
                        badge.style.backgroundColor = badgeColor;
                        popup.remove();
                        badge.classList.remove('badge-clicked');
                        badgeClicked = false;
                        return;
                    }
                    // create a popup below this element
                    let popup = document.createElement('div');
                    popup.classList.add('popup');
                    popup.style.position = 'absolute';
                    popup.style.width = '70ch';
                    popup.style.backgroundColor = '#fff';
                    popup.style.padding = '10px 16px';
                    popup.style.borderRadius = '10px';
                    popup.style.zIndex = '1000';
                    popup.style.maxWidth = 'fit-content';
                    popup.style.border = '1px solid #D9D9D9'
                    popup.style.fontSize = '14px';
                    popup.innerHTML = `<span>This review is ${random}% trustworthy. The review lacks specificity and uses generic language, which is common in less trustworthy reviews.</span>`;
                    badgeWrapper.appendChild(popup);
                    badge.style.backgroundColor = clickedBadgeColor;

                    badgeClicked = true;
                    badge.classList.add('badge-clicked');

                });
            }
        }
    });
}

document.getElementById('myButton').addEventListener('click', detectFakeReviews);


async function detectFakeReviews2() {
    let [tab] = await chrome.tabs.query({ active: true });
    console.log(tab);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: async () => {
            function getDescriptionBody() {
                let description = document.getElementById('description-body');
                return description;
            }

            function getSpecifications() {
                let specifications = document.getElementsByClassName('specifications-body')[0];
                return specifications;
            }

            function getReviewRows() {
                return document.getElementsByClassName('product-review-item');
            }
            let reviewRows = getReviewRows();
            
            let reviews = [];
            // get data
            for(let reviewRow of reviewRows) {
                
                let id = reviewRow.getAttribute('data-id');
                console.log('id', id);
                let userData = reviewRow.getElementsByClassName('product-review-user-meta')[0];
                // author name is the first p tag
                let author_name = userData.getElementsByTagName('p')[0].innerText;
                // review date is the second p tag
                let published_on = new Date(userData.getElementsByTagName('p')[1].innerText);
                let author_id = reviewRow.getElementsByClassName('product-review-user-avatar')[0].getElementsByTagName('a')[0].href.split('/').pop();
                let title = reviewRow.getElementsByClassName('product-review-title')[0].innerText;
                let description = reviewRow.getElementsByClassName('review-body-container')[0].innerText;
                let rating = reviewRow.getElementsByClassName('star-rating-inner')[0];
                rating = parseInt(rating.style.width.split('%')[0]) / 20;

                let votes = Number(reviewRow.getElementsByClassName('vote-review-text')[0].innerText);
                let has_bought_product = Boolean(reviewRow.getElementsByClassName('em-verified text-success')[0]);

                reviews.push({
                    id,
                    author_name,
                    published_on,
                    author_id,
                    title,
                    description,
                    rating,
                    votes,
                    has_bought_product
                });
            }

            try {
                await fetch('http://localhost:8000/review', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        description: getDescriptionBody().innerText,
                        specifications: getSpecifications().innerText,
                        reviews
                    }),
                })
            } catch (error) {
                console.error(error);
            }


            // loop through all elements
            for (let reviewRow of reviewRows) {


                // create a random value between 1 and 100
                let random = Math.floor(Math.random() * 100);

                reviewRow.style.backgroundColor = random <= 30 ? '#DF221414' : random > 31 && random < 70 ? '#FBC02D14' : '#1B870014';

                const badgeColor = random <= 30 ? '#DF2214' : random > 31 && random < 70 ? '#FBC02D' : '#1B8700';
                const clickedBadgeColor = random <= 30 ? '#B21B10' : random > 31 && random < 70 ? '#E2AD29' : '#187A00';

                let badgeWrapper = document.createElement('div');
                badgeWrapper.style.display = 'inline-block';
                badgeWrapper.style.marginLeft = '24px';
                badgeWrapper.innerHTML =`<p class="badge">
                                        ${random}% Trustworthy
                                    </p>

                                    <style>
                                        .badge {
                                            border-radius: 40px;
                                            height: 32px;
                                            padding: 8.5px 20px;
                                            width: max-content;
                                            display: flex;
                                            align-items: center;
                                            cursor: pointer;
                                        }
                                        .badge-clicked {
                                            background: "purple";
                                        }
                                    </style>`;
                                    
                reviewRow.getElementsByClassName('star-rating-container')[0].appendChild(badgeWrapper);
                let badge = badgeWrapper.getElementsByClassName('badge')[0];
                badge.style.backgroundColor = badgeColor;
                badge.style.color= random > 31 && random < 70 ? '#000' : '#fff';
                let badgeClicked = false;
                badge.addEventListener('click', () => {
                    if (badgeClicked) {
                        let popup = badgeWrapper.getElementsByClassName('popup')[0];
                        badge.style.backgroundColor = badgeColor;
                        popup.remove();
                        badge.classList.remove('badge-clicked');
                        badgeClicked = false;
                        return;
                    }
                    // create a popup below this element
                    let popup = document.createElement('div');
                    popup.classList.add('popup');
                    popup.style.position = 'absolute';
                    popup.style.width = '70ch';
                    popup.style.backgroundColor = '#fff';
                    popup.style.padding = '10px 16px';
                    popup.style.borderRadius = '10px';
                    popup.style.zIndex = '1000';
                    popup.style.maxWidth = 'fit-content';
                    popup.style.border = '1px solid #D9D9D9'
                    popup.style.fontSize = '14px';
                    popup.innerHTML = `<span>This review is ${random}% trustworthy. The review lacks specificity and uses generic language, which is common in less trustworthy reviews.</span>`;
                    badgeWrapper.appendChild(popup);
                    badge.style.backgroundColor = clickedBadgeColor;

                    badgeClicked = true;
                    badge.classList.add('badge-clicked');

                });
            }
        }
    });
}

document.getElementById('myButton2').addEventListener('click', detectFakeReviews2);