const expandButton = document.querySelector('.expand-button');
const habitForm = document.querySelector('.habit-form');
const habitsSection = document.querySelector('.habits');
const calendar = document.querySelector('.calendar');
const invalidHabitInput = document.querySelector('.is-invalid');
const formErrorMsg = document.querySelector('.form-error');

const hideHabitSection = () => {
  habitsSection.style.display = 'block';
};

const toggleHabitsForm = () => {
  habitForm.classList.toggle('expand-form');
  if (habitForm.classList.contains('expand-form')) {
    expandButton.textContent = '━';
    habitsSection.style.display = 'none';
  } else {
    expandButton.textContent = '╋';
    setTimeout(hideHabitSection, 260);
    if (formErrorMsg) {
      invalidHabitInput.classList.remove('is-invalid');
      formErrorMsg.remove();
    }
  }
};

expandButton.addEventListener('click', toggleHabitsForm);

// center calendar scroll
const setCalendarScroll = () => {
  calendar.scrollTo({
    left: (calendar.scrollWidth - calendar.clientWidth) / 2,
  });
};

setCalendarScroll();

window.addEventListener('resize', setCalendarScroll);

// Form error
const re = /\b.{3,}/;
const validateHabitInput = () => {
  if (!re.test(invalidHabitInput.value)) {
    invalidHabitInput.classList.add('is-invalid');
    formErrorMsg.style.display = 'inline';
  } else {
    invalidHabitInput.classList.remove('is-invalid');
    formErrorMsg.style.display = 'none';
  }
};

const checkFormError = () => {
  if (formErrorMsg) {
    habitForm.classList.add('expand-form');
    expandButton.textContent = '━';
    habitsSection.style.display = 'none';
    validateHabitInput();
    invalidHabitInput.addEventListener('input', validateHabitInput);
  }
};
checkFormError();
