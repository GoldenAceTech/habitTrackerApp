const invalidHabitInput = document.querySelector('.is-invalid');
const formErrorMsg = document.querySelector('.form-error');

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

if (formErrorMsg) {
  validateHabitInput();
  invalidHabitInput.addEventListener('input', validateHabitInput);
}

const expandButton = document.querySelector('.expand-button');
const habitForm = document.querySelector('.habit-form');
const habitsSection = document.querySelector('.habits');

const toggleDisplay = () => {
  habitsSection.style.display = 'block';
};

const toggleHabitsForm = () => {
  habitForm.classList.toggle('expand-form');
  if (habitForm.classList.contains('expand-form')) {
    expandButton.textContent = '━';
    habitsSection.style.display = 'none';
  } else {
    expandButton.textContent = '╋';
    setTimeout(toggleDisplay, 260);
  }
};

expandButton.addEventListener('click', toggleHabitsForm);

const calendar = document.querySelector('.calendar');

const setCalendarScroll = () => {
  calendar.scrollTo({
    left: (calendar.scrollWidth - calendar.clientWidth) / 2,
  });
};

setCalendarScroll();

window.addEventListener('resize', setCalendarScroll);
