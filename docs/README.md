# Documentation

<div id="documentation"></div>

<script>
    async function fetchAndDisplayDocumentation() {
        try {
            const response = await fetch('config.json');
            const jsonData = await response.json();

            createDocumentation(jsonData);
        } catch (error) {
            console.error('Error fetching JSON:', error);
        }
    }

    function createDocumentation(data) {
        const documentationDiv = document.getElementById('documentation');

        const h1 = document.createElement('h1');
        h1.textContent = data.name;
        documentationDiv.appendChild(h1);

        data.methods.forEach(method => {
            const h2 = document.createElement('h2');
            h2.textContent = method.name;
            documentationDiv.appendChild(h2);

            const p = document.createElement('p');
            p.textContent = `Method ${method.name}.`;
            documentationDiv.appendChild(p);

            if (method.parameters.length > 0) {
                const h3 = document.createElement('h3');
                h3.textContent = 'Parameters';
                documentationDiv.appendChild(h3);

                const ul = document.createElement('ul');
                method.parameters.forEach(parameter => {
                    const li = document.createElement('li');
                    li.textContent = parameter;
                    ul.appendChild(li);
                });
                documentationDiv.appendChild(ul);
            }
        });
    }

    fetchAndDisplayDocumentation();
</script>
