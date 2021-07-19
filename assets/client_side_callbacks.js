function UpdateEIP1559ByScenarios (EIP1559Dropdown) {
    EIP1559Scenarios = {'Disabled': 0, 'Enabled: Steady State': 100, 'Enabled: MEV':70};
    if (EIP1559Dropdown === 'Custom'){
        return window.dash_clientside.no_update
    }
    return EIP1559Scenarios[EIP1559Dropdown];
}

function UpdateValidatorAdoptionSlidersByScenarios (ValidatorDropdown) {
    ValidatorScenarios = {'Normal Adoption': 3, 'Low Adoption': 1.5, 'High Adoption':4.5};
    if (ValidatorDropdown === 'Custom'){
        return window.dash_clientside.no_update
    }
    return ValidatorScenarios[ValidatorDropdown];
}

console.log(UpdateValidatorAdoptionSlidersByScenarios('Normal Adoption'));
