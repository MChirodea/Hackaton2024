async function detectFakeReviews() {
    let [tab] = await chrome.tabs.query({ active: true });
    console.log(tab);
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            // get all elements with class 'product-review-item'
            let elements = document.getElementsByClassName('product-review-item');

            // loop through all elements
            for (let element of elements) {
                
                // change the background color of the element
                element.style.position = 'relative';

                // create a random boolean variable to decide if the element will have a checkmark or not
                let random = Math.random() >= 0.5;

                // create a small div element on top right corner of the element with a checkark icon
                let div = document.createElement('div');
                div.classList.add('customDiv');
                div.style.position = 'absolute';
                div.style.top = '0';
                div.style.right = '0';
                div.style.backgroundColor = random ? 'green' : 'red';
                div.style.color = 'white';
                div.style.padding = '5px';
                div.innerHTML = random ? '✓' : 'X';
                element.appendChild(div);
                
                
            }

        }
    });
}

document.getElementById('myButton').addEventListener('click', detectFakeReviews);