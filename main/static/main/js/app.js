document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }

      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
      this.no_bags = parseInt(document.querySelector('.step2 .form-group--inline').
          children[0].children[0].value);
      // after step 1
      if(this.currentStep == 2) {
        let inputs = document.querySelectorAll('.step1 .form-group--checkbox');
        this.categories_ids = [];
        this.categories_names = [];
        inputs.forEach(el => {
          if(el.children[0].children[0].checked === true){
            this.categories_ids.push(parseInt(el.children[0].children[0].value,10));
            this.categories_names.push(el.children[0].children[2].textContent);
          }
        });
      }

      // before step 3
      if (this.currentStep == 3) {
        let inputs = document.querySelectorAll('.step3 .form-group--checkbox #categories');
        inputs.forEach(input => {
          input.parentElement.style.display = 'none';
          let institutions_categories_ids = [];
          input.value.toString().split(',').forEach(el => {
          let value = parseInt(el, 10);
          if(!isNaN(value)){
            institutions_categories_ids.push(value);
          }
        });
          let bool = true;
          this.categories_ids.forEach(id => {
            if(!institutions_categories_ids.includes(id)){
              bool = false;
            }
          });
          if(bool){
          input.parentElement.style.display = 'block';
          }
        });
      }
        // after step 3
      if(this.currentStep == 4){
        let divs = document.querySelectorAll('.step3 .form-group--checkbox');
        let inputs = [];
        divs.forEach(div => {
          inputs.push(div.children[0].children[0])
        });
        inputs.forEach(input => {
          if(input.checked === true){
            this.institution_id = input.value;
            this.institution_name = input.parentElement.children[2].children[0].textContent;
          }
        });
      }


      if(this.currentStep == 5) {
        // after step 4
        this.address = {};
        this.delivery = {};

        let step4 = document.querySelector('.step4 .form-section--columns');

        let street = step4.querySelector('#address');
        this.address['street'] = street.value;

        let city = step4.querySelector('#city');
        this.address['city'] = city.value;

        let postcode = step4.querySelector('#postcode');
        this.address['postcode'] = postcode.value;

        let phone = step4.querySelector('#phone');
        this.address['phone'] = phone.value;

        let date = step4.querySelector('#date');
        this.delivery['date'] = date.value;

        let time = step4.querySelector('#time');
        this.delivery['time'] = time.value;

        let more_info = step4.querySelector('#more_info');
        this.delivery['more_info'] = more_info.value;

        // before step 5

        let bags = document.querySelector('.bags');
        // zmien słowo worki żeby się odmieniało
        bags.textContent = this.no_bags + " worki";

        let institution = document.querySelector('.institution');
        institution.textContent = this.institution_name;

        let address_ = document.querySelector('.address');
        let ul = address_.children[1];

        ul.children[0].textContent = this.address.street;

        ul.children[1].textContent = this.address.city;

        ul.children[2].textContent = this.address.postcode;

        ul.children[3].textContent = this.address.phone;

        let delivery_ = document.querySelector('.delivery');
        ul = delivery_.children[1];

        ul.children[0].textContent = this.delivery.date;

        ul.children[1].textContent = this.delivery.time;

        ul.children[2].textContent = this.delivery.more_info;
      }

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
