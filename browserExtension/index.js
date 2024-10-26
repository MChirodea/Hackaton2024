

async function detectFakeReviews() {
    let [tab] = await chrome.tabs.query({ active: true });
    console.log(tab);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            function getDescriptionBody() {
                // get all reviews text by class name 'review-body-container'
                let description = document.getElementById('description-body');
            
                console.log(description);
                console.log(description.innerText);

                return description;
            }

            function getReviewRows() {
                return document.getElementsByClassName('product-review-item');
            }

            function getSpecifications() {
                let specifications = document.getElementsByClassName('specifications-body')[0];
                console.log(specifications);
                console.log(specifications.innerText);
                return specifications;
            }


            getDescriptionBody();
            getSpecifications();

            let currentLocation = window.location.href;
            console.log(currentLocation);
            let reviewRows = getReviewRows();

            fetch('http://localhost:8000/send-ext-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: currentLocation,
                    description: getDescriptionBody().innerText,
                    specifications: getSpecifications().innerText
                }),
            })

            // loop through all elements
            for (let element of reviewRows) {
                
                // change the background color of the element
                element.style.position = 'relative';

                // create a random value between 1 and 100
                let random = Math.floor(Math.random() * 100);

                element.style.backgroundColor = random <= 30 ? '#DF221414' : random > 31 && random < 70 ? '#FBC02D14' : '#1B870014';

                const badgeColor = random <= 30 ? '#DF2214' : random > 31 && random < 70 ? '#FBC02D' : '#1B8700';
                console.log(badgeColor);

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
                                            padding: 0 20px;
                                            width: max-content;
                                            display: flex;
                                            align-items: center;
                                        }
                                    </style>`;
                                    
                element.getElementsByClassName('star-rating-container')[0].appendChild(badgeWrapper);
                let badge = badgeWrapper.getElementsByClassName('badge')[0];
                badge.style.backgroundColor = badgeColor;
                badge.style.color= random > 31 && random < 70 ? '#000' : '#fff';
            }
        }
    });
}

document.getElementById('myButton').addEventListener('click', detectFakeReviews);