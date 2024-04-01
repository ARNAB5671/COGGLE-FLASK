document.addEventListener('DOMContentLoaded', function() {
    const extrasContainer = document.getElementById('extras-container');
    const addExtraBtn = document.getElementById('add-extra-btn');

    addExtraBtn.addEventListener('click', function() {
        const newExtraItem = document.createElement('div');
        newExtraItem.classList.add('extra-item');
        newExtraItem.innerHTML = `
            <input type="text" class="extra" name="extras[]" required>
            <input type="number" class="price" name="prices[]" required>
            <button type="button" class="remove-extra-btn">Remove</button>
        `;
        extrasContainer.appendChild(newExtraItem);
    });

    extrasContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-extra-btn')) {
            event.target.parentElement.remove();
        }
    });

    const form = document.getElementById('manager-form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        
        const today = new Date().toISOString().split('T')[0];
        // Serialize form data
        const formData = new FormData(form);

        // Convert form data to JSON object
        const jsonData = { date: today }; // Add today's date to the JSON object
        formData.forEach((value, key) => {
            if (!jsonData[key]) {
                jsonData[key] = [];
            }
            jsonData[key].push(value);
        });

        // Send POST request with JSON data to the server
        fetch('http://127.0.0.1:5000/setMeal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Form submitted successfully:', data);
            // Handle response as needed
            if (data.success) {
                // Disable form fields if success is true
                Array.from(form.elements).forEach(element => {
                    element.disabled = true;
                });
            } else {
                // Alert the user with the message from the response
                alert(data.message);
            }
    
        })
        .catch(error => {
            console.error('Error:', error);
            // Handle error
        });
    });
});