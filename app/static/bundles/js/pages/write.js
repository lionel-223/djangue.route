if (document.getElementById("write-a-letter")) {
  const gender_selects = document.querySelectorAll("#gender-select .select")
  const is_male_input = document.querySelector('[name="is_male"]');

  function refreshActiveGenderSelect() {
      for (let e of gender_selects) {
        if (is_male_input.value == e.dataset.isMale)
          e.classList.add('active');
        else
          e.classList.remove('active');
      }
  }

  refreshActiveGenderSelect();
  for (let current of gender_selects) {
    current.onclick = function () {
      is_male_input.value = current.dataset.isMale;
      refreshActiveGenderSelect();
    };
  }


  async function setCountryCode() {
    // Uses ipapi.co to get the user's country and prefill the country select

    const country_code_input = document.querySelector('[name="country_code"]');
    if (country_code_input.value != "0")
      return;
    let ipapi_result = await fetch('https://ipapi.co/json/');
    ipapi_result = await ipapi_result.json();
    console.log(`country_code ${ipapi_result.country}`);
    country_code_input.value = ipapi_result.country;
  }
  setCountryCode();
}
