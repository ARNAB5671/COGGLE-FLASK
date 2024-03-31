document.addEventListener('DOMContentLoaded', function() {
    let selectButtons = document.querySelectorAll('.select-btn');
    const totalAmountElement = document.getElementById('total-amount');
    const baseMealElement = document.querySelector('.base-meals');
    const baseMealAmountElement = document.querySelector('.base-meal-amount');
    const baseMealAmount = parseFloat(baseMealAmountElement.textContent.match(/\d+/)[0]);
    const extraMealAmountElement = document.getElementById('total-amount');
    const sendRequestBtn = document.getElementById('sendRequestBtn');
    let totalAmount = 0;

    const finalAmountElement = document.getElementById('final-amount');
    finalAmountElement.textContent = baseMealAmount;

    // get the values of meals from the api
    fetch('http://127.0.0.1:5000/todaysMealOptions') // Replace 'https://api.example.com/data' with the actual URL
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Assuming the response is JSON data
    })
    .then(data => {
        console.log('Data:', data);
        // Handle the data received from the API
        document.getElementById('base-meals').textContent = data.mealOptions.baseMeal;
        document.getElementById('base-meal-amount').textContent = 'Base: Rs ' + data.mealOptions.baseMealPrice + '/-';
        
        const extrasList = data.mealOptions.extrasList;
        const extrasListElement = document.getElementById('extra-meal-list');
        extrasList.forEach(item => {
            for (const [food, price] of Object.entries(item)) {
                const listItem = document.createElement('li');
                listItem.setAttribute('data-price', price);
                
                listItem.innerHTML = food + ' (<span class="price">Rs ' + price + '/-</span>) <button class="select-btn">Select</button>';
                listItem.style.display = 'block';
                extrasListElement.appendChild(listItem);
            }
        });

        selectButtons = document.querySelectorAll('.select-btn');

        console.log(selectButtons);

    })
    .catch(error => {
        console.error('Error:', error);
        // Handle any errors that occurred during the fetch
    });

    sendRequestBtn.addEventListener('click', function() {
        const baseMeal = baseMealElement.textContent.trim();
        // const baseMealAmount = parseFloat(baseMealAmountElement.textContent.match(/\d+/)[0]);
        // const extraMealPrice = parseFloat(extraMealAmountElement.textContent.match(/\d+/)[0]);
        // Get today's date
        const today = new Date();
        const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();

        const requestBody = {
            'baseMeal': baseMeal,
            'baseMealAmount': baseMealAmount,
            'extraMealPrice': totalAmount,
            'totalAmount': baseMealAmount + totalAmount,
            'date': date
        };
        fetch('http://127.0.0.1:5000/studentSelectMeals', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response:', data);
            // Handle response as needed
            console.log('TEST');
            const elementsToRemove = document.querySelectorAll('.select-btn');
            elementsToRemove.forEach(element => {
                element.remove();
            });
            const elementsToRemove2 = document.querySelectorAll('.deselect-btn');
            elementsToRemove2.forEach(element => {
                element.remove();
            });

        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
    });


    document.querySelector('.extras-box').addEventListener('click', function(event) {
        if (event.target.classList.contains('select-btn')) {
            const button = event.target;
            const listItem = button.parentElement;
            const price = parseFloat(listItem.getAttribute('data-price'));
            if (listItem.classList.contains('selected')) {
                totalAmount -= price;
                listItem.classList.remove('selected');
                button.textContent = 'Select';
                listItem.querySelector('.deselect-btn').remove(); // Remove the deselect button if it exists
            } else {
                totalAmount += price;
                listItem.classList.add('selected');
                button.textContent = 'Deselect';
                const deselectButton = document.createElement('button');
                deselectButton.textContent = 'Deselect';
                deselectButton.classList.add('deselect-btn');
                deselectButton.addEventListener('click', function() {
                    totalAmount -= price;
                    listItem.classList.remove('selected');
                    button.textContent = 'Select';
                    listItem.querySelector('.deselect-btn').remove();
                    totalAmountElement.textContent = totalAmount;
                    finalAmountElement.textContent = baseMealAmount + totalAmount;
                });
                listItem.appendChild(deselectButton);
            }
            totalAmountElement.textContent = totalAmount;
            finalAmountElement.textContent = baseMealAmount + totalAmount;
        }
    });
});
