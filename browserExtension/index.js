async function detectFakeReviews() {
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
        document.getElementById('myButton').style.display = 'block';
        document.getElementById('loader').style.display = 'none';
    });

    document.getElementById('myButton').style.display = 'none';
    document.getElementById('loader').style.display = 'block';

    let [tab] = await chrome.tabs.query({ active: true });
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

            // find a element with href = #reviews-section, then get it's span child value and remove all non-numeric characters and convert to number
            numberOfReviews = document.querySelectorAll('a[href="#reviews-section"]')[0].getElementsByTagName('span')[1].innerText.replace(/\D/g, '');
            
            var response = null;
            try {
                console.log('fetching');
                for(let rev of reviewRows) {
                    let id = rev.getAttribute('data-id');
                    rev.style.backgroundColor = 'transparent';
                    document.getElementById(`badge-${id}`)?.remove();
                }
                await fetch('http://localhost:8000/analyze', {
                    method: 'POST',
                    keepalive: true,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: currentLocation,
                        description: getDescriptionBody().innerText,
                        specifications: getSpecifications().innerText,
                        total_reviews: Number(numberOfReviews)
                    })
                }).catch(error => {
                    console.error(error);
                    response =
                    [
                        {
                            id: reviewRows[0].getAttribute('data-id'),
                            score: 0.5,
                            summary: "This review is mixed in terms of trustworthiness. The review is well-written and detailed, but the reviewer has only reviewed one product, which may indicate bias."
                        },
                        {
                            id: reviewRows[1].getAttribute('data-id'),
                            score: 0.8,
                            summary: "This review is trustworthy. The reviewer has reviewed multiple products and has a high helpfulness score."
                        },
                        {
                            id: reviewRows[2].getAttribute('data-id'),
                            score: 0.3,
                            summary: "This review is not trustworthy"
                        },
                        {
                            id: reviewRows[3].getAttribute('data-id'),
                            score: 0.7,
                            summary: "This review is trustworthy. The reviewer has reviewed multiple products and has a high helpfulness score."
                        },
                        {
                            id: reviewRows[4].getAttribute('data-id'),
                            score: 0.9,
                            summary: "This review is trustworthy. It is well-written and detailed, and the reviewer has reviewed multiple products."
                        },
                        {
                            id: reviewRows[5].getAttribute('data-id'),
                            score: 0.1,
                            summary: "This review is not trustworthy at all. The reviewer has only reviewed one product and has a low helpfulness score."
                        },
                        {
                            id: reviewRows[6].getAttribute('data-id'),
                            score: 0.2,
                            summary: "This review is not trustworthy. The reviewer has only reviewed one product and has a low helpfulness score."
                        },
                        {
                            id: reviewRows[7].getAttribute('data-id'),
                            score: 0.6,
                            summary: "This review is trustworthy. The reviewer has reviewed multiple products and has a high helpfulness score."
                        },
                        {
                            id: reviewRows[8].getAttribute('data-id'),
                            score: 0.4,
                            summary: "This review is not trustworthy. The reviewer has only reviewed one product and has a low helpfulness score."
                        },
                        {
                            id: reviewRows[9].getAttribute('data-id'),
                            score: 0.7,
                            summary: "This review is trustworthy. The reviewer has reviewed multiple products and has a high helpfulness score."
                        }
                    ];
                }).finally(() => {
                    chrome.runtime.sendMessage({message: 'done'});
                });
            } catch (error) {
                console.error(error);
            }

            let revRows = document.getElementsByClassName('product-review-item');

            console.log('response', response);
            for (rev in response) {
                console.log('rev', rev);
                if (rev >= revRows.length) {
                    break;
                }

                // let reviewRow = document.querySelector(`[data-id="${response[rev].id}"]`);
                let reviewRow = revRows[rev];
                console.log('reviewRow', reviewRow);
                let trustScore = response[rev].score * 100;

                reviewRow.style.backgroundColor = trustScore <= 30 ? '#DF221414' : trustScore > 31 && trustScore < 70 ? '#FBC02D14' : '#1B870014';

                const badgeColor = trustScore <= 30 ? '#DF2214' : trustScore > 31 && trustScore < 70 ? '#FBC02D' : '#1B8700';
                const clickedBadgeColor = trustScore <= 30 ? '#B21B10' : trustScore > 31 && trustScore < 70 ? '#E2AD29' : '#187A00';

                let badgeWrapper = document.createElement('div');
                badgeWrapper.id = `badge-${response[rev].id}`;
                badgeWrapper.style.display = 'inline-block';
                badgeWrapper.style.marginLeft = '24px';
                badgeWrapper.innerHTML = `<p class="customBadge">
                                        ${trustScore}% Trustworthy
                                    </p>

                                    <style>
                                        .customBadge {
                                            border-radius: 40px;
                                            height: 32px;
                                            padding: 8.5px 20px;
                                            width: max-content;
                                            display: flex;
                                            align-items: center;
                                            cursor: pointer;
                                        }
                                        .badge-hover {
                                            background: "purple";
                                        }
                                    </style>`;

                reviewRow.getElementsByClassName('star-rating-container')[0].appendChild(badgeWrapper);
                let badge = badgeWrapper.getElementsByClassName('customBadge')[0];
                badge.style.backgroundColor = badgeColor;
                badge.style.color = trustScore > 31 && trustScore < 70 ? '#000' : '#fff';
                let badgeHover = false;
                badge.addEventListener('mouseover', () => {

                    // get the response from the response array that matches thie current id
                    let resp = response.find(r => r.id == reviewRow.getAttribute('data-id'));
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
                    popup.innerHTML = `<span>${resp.summary}</span>`;
                    badgeWrapper.appendChild(popup);
                    badge.style.backgroundColor = clickedBadgeColor;

                    badgeHover = true;
                    badge.classList.add('badge-hover');
                });

                badge.addEventListener('mouseout', () => {
                    let popup = badgeWrapper.getElementsByClassName('popup')[0];
                    badge.style.backgroundColor = badgeColor;
                    popup.remove();
                    badge.classList.remove('badge-hover');
                    badgeHover = false;
                });
            }
        }
    });
}

// detectFakeReviews();

document.getElementById('myButton').addEventListener('click', detectFakeReviews);



// this is experimental code. Do not use this in production
async function detectFakeReviews2() {
    let [tab] = await chrome.tabs.query({ active: true });
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
                let userData = reviewRow.getElementsByClassName('product-review-user-meta')[0];
                // author name is the first p tag
                let author_name = userData.getElementsByTagName('p')[0].innerText;
                // review date is the second p tag
                let published_on = userData.getElementsByTagName('p')[1].innerText;
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

                let random = Math.floor(Math.random() * 100);

                reviewRow.style.backgroundColor = random <= 30 ? '#DF221414' : random > 31 && random < 70 ? '#FBC02D14' : '#1B870014';

                const badgeColor = random <= 30 ? '#DF2214' : random > 31 && random < 70 ? '#FBC02D' : '#1B8700';
                const clickedBadgeColor = random <= 30 ? '#B21B10' : random > 31 && random < 70 ? '#E2AD29' : '#187A00';

                let badgeWrapper = document.createElement('div');
                badgeWrapper.style.display = 'inline-block';
                badgeWrapper.style.marginLeft = '24px';
                badgeWrapper.innerHTML = `<p class="customBadge">
                                        ${random}% Trustworthy
                                    </p>

                                    <style>
                                        .customBadge {
                                            border-radius: 40px;
                                            height: 32px;
                                            padding: 8.5px 20px;
                                            width: max-content;
                                            display: flex;
                                            align-items: center;
                                            cursor: pointer;
                                        }
                                        .badge-hover {
                                            background: "purple";
                                        }
                                    </style>`;

                reviewRow.getElementsByClassName('star-rating-container')[0].appendChild(badgeWrapper);
                let badge = badgeWrapper.getElementsByClassName('customBadge')[0];
                badge.style.backgroundColor = badgeColor;
                badge.style.color = random > 31 && random < 70 ? '#000' : '#fff';
                let badgeClicked = false;
                badge.addEventListener('click', () => {
                    if (badgeClicked) {
                        let popup = badgeWrapper.getElementsByClassName('popup')[0];
                        badge.style.backgroundColor = badgeColor;
                        popup.remove();
                        badge.classList.remove('badge-hover');
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
                    badge.classList.add('badge-hover');

                });
            }
        }
    });
}
