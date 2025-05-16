flatpickr('#datePicker', {
    inline: true,
    locale: 'ru'
});

flatpickr('#timePicker', {
  enableTime: true,
  noCalendar: true,
  dateFormat: "H:i",
  time_24hr: true,    // Явное указание 24-часового формата
  static: true,       // Если нужно показать сразу
  defaultHour: 8      // Стартовое время
});

class TimePicker {
  constructor(container, isHours = false) {
    this.container = container;
    this.valuesContainer = container.querySelector('.values');
    this.isHours = isHours;
    this.max = isHours ? 23 : 59;
    this.current = 0;

    this.render();
    this.addListeners();
  }

  getFormatted(value) {
    return value.toString().padStart(2, '0');
  }

  render() {
    const range = 2; // сколько значений вверх/вниз от текущего
    const values = [];

    for (let i = -range; i <= range; i++) {
      const val = (this.current + i + this.max + 1) % (this.max + 1);
      values.push(`<div class="value${i === 0 ? ' current' : ''}">${this.getFormatted(val)}</div>`);
    }

    this.valuesContainer.innerHTML = values.join('');
    this.valuesContainer.style.transform = `translateY(-${2 * 2}em)`; // центральный элемент по центру
  }

  scroll(direction) {
    this.valuesContainer.style.transition = 'transform 0.3s ease';
    this.valuesContainer.style.transform = `translateY(-${(2 + direction) * 2}em)`;

    setTimeout(() => {
      this.current = (this.current + direction + this.max + 1) % (this.max + 1);
      this.render();
      this.valuesContainer.style.transition = 'none';
    }, 300);
  }

  addListeners() {
    this.container.addEventListener('wheel', (e) => {
      e.preventDefault();
      this.scroll(Math.sign(e.deltaY));
    });

    let startY;
    this.container.addEventListener('touchstart', (e) => {
      startY = e.touches[0].clientY;
    });

    this.container.addEventListener('touchmove', (e) => {
      const deltaY = e.touches[0].clientY - startY;
      if (Math.abs(deltaY) > 30) {
        this.scroll(Math.sign(deltaY));
        startY = e.touches[0].clientY;
      }
    });
  }
}

new TimePicker(document.querySelector('.hours'), true);
new TimePicker(document.querySelector('.minutes'));

// class TimePicker {
//   constructor(container, isHours = false) {
//     this.container = container;
//     this.isHours = isHours;
//     this.max = isHours ? 23 : 59;
//     this.min = 0;
//     this.current = parseInt(container.querySelector('.current').textContent);
//     this.updateValues();
//     this.addEventListeners();
//   }

//   updateValues() {
//     const prev = (this.current - 1 + this.max + 1) % (this.max + 1);
//     const next = (this.current + 1) % (this.max + 1);
    
//     this.container.querySelector('.prev').textContent = 
//       prev.toString().padStart(2, '0');
//     this.container.querySelector('.current').textContent = 
//       this.current.toString().padStart(2, '0');
//     this.container.querySelector('.next').textContent = 
//       next.toString().padStart(2, '0');
//   }

//   scroll(direction) {
//     this.current = (this.current + direction + this.max + 1) % (this.max + 1);
//     this.updateValues();
//     this.playAnimation(direction);
//   }

//   playAnimation(direction) {
//     const elements = this.container.children;
//     elements[0].style.transform = `translateY(${direction * 100}%)`;
//     elements[2].style.transform = `translateY(${-direction * 100}%)`;
    
//     setTimeout(() => {
//       elements[0].style.transition = 'none';
//       elements[2].style.transition = 'none';
      
//       this.updateValues();
      
//       elements[0].style.transform = 'translateY(-100%)';
//       elements[2].style.transform = 'translateY(100%)';
      
//       setTimeout(() => {
//         // elements[0].style.transition = 'transform 0.3s ease, opacity 0.3s ease';
//         // elements[2].style.transition = 'transform 0.3s ease, opacity 0.3s ease';
//         elements[0].style.transition = 'transform 0.3s ease, opacity 0.3s ease';
//         elements[2].style.transition = 'transform 0.3s ease, opacity 0.3s ease';
//       }, 10);
//     }, 300);
//   }

//   addEventListeners() {
//     let startY;
//     const handleWheel = (e) => {

//       e.preventDefault();
//       this.scroll(Math.sign(e.deltaY));
//     };

//     const handleTouchStart = (e) => {
//       startY = e.touches[0].clientY;
//     };

//     const handleTouchMove = (e) => {
//       const deltaY = e.touches[0].clientY - startY;
//       if (Math.abs(deltaY) > 30) {
//         this.scroll(Math.sign(deltaY));
//         startY = e.touches[0].clientY;
//       }
//     };

//     this.container.addEventListener('wheel', handleWheel);
//     this.container.addEventListener('touchstart', handleTouchStart);
//     this.container.addEventListener('touchmove', handleTouchMove);
//   }
// }

// // Инициализация
// const hoursPicker = new TimePicker(document.querySelector('.hours'), true);
// const minutesPicker = new TimePicker(document.querySelector('.minutes'));