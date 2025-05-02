class NavbarElement{
    constructor(name, title, iconUrl, href) {
        this.name = name;
        this.title = title;
        this.iconUrl = iconUrl;
        this.href = href;

        this.isActive = false;
    }

    create(){

        let color = 'white';

        //получение цветов из css
        const styles = getComputedStyle(document.documentElement)
        const primaryColor = styles.getPropertyValue('--primary-color')


        //Создание элементов
        this.navbarElement = document.createElement('a');
        this.navbarElement.classList.add('navbar-element');

        const iconContainer = document.createElement('div');
        iconContainer.classList.add('icon-container');

        const title = document.createElement('p');
        title.textContent = this.title;

        this.navbarElement.appendChild(iconContainer);
        this.navbarElement.appendChild(title);

        if(this.isActive) {
            color = primaryColor;
            this.navbarElement.classList.add('navbar-element-active');
        }


        fetch(this.iconUrl)
            .then(response => response.text())
            .then(svgText => {
                iconContainer.innerHTML = svgText;

                const paths = iconContainer.querySelectorAll('path');

                paths.forEach(path => {
                    const hasFill = path.hasAttribute('fill');
                    const hasStroke = path.hasAttribute('stroke');

                    if (hasFill && path.getAttribute('fill') !== 'none') {
                        path.setAttribute('fill', color);
                    }

                    if (hasStroke && path.getAttribute('stroke') !== 'none') {
                        path.setAttribute('stroke', color);
                    }
                });
            });
    }
}

class Navbar{
    constructor(items) {
        this.navbarElements = [];

        items.forEach(item => {
            this.navbarElements.push(new NavbarElement(item.name, item.title, item.icon, item.href));
        });

    }

    setActive(itemName){
        this.navbarElements.forEach(item => {
            if(item.name === itemName){
                item.isActive = true;
            }
        });
    }

    create(){
        this.navbarElements.forEach(item => {
            item.create();

            const navbar = document.getElementById('navbar');

            navbar.appendChild(item.navbarElement);

        });
    }
}
