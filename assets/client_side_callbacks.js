window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_max_validator_cap_slider_function: function(MaxValidatorCapDropdown) {
            MaxValidatorScenarios = {'No Validator Cap': 0, "Vitalik's proposal (max 524,288 validators)": 524}
            if (MaxValidatorCapDropdown === 'Custom Value'){
                return window.dash_clientside.no_update
            }
            return MaxValidatorScenarios[MaxValidatorCapDropdown]
        },
        update_eip1559_slider_function: function(EIP1559Dropdown) {
            EIP1559Scenarios = {'Disabled (Base Fee = 0)': 0, 'Enabled (Base Fee = 30)': 30}
            if (EIP1559Dropdown === 'Enabled (Custom Value)'){
                return window.dash_clientside.no_update
            }
            return EIP1559Scenarios[EIP1559Dropdown];
        },
        update_eip1559_priority_fee_slider_function: function(EIP1559Dropdown) {
            EIP1559Scenarios = {'Disabled (Priority Fee = 0)': 0, 'Enabled (Priority Fee = 2)': 2}
            if (EIP1559Dropdown === 'Enabled (Custom Value)'){
                return window.dash_clientside.no_update
            }
            return EIP1559Scenarios[EIP1559Dropdown];
        },
        update_pos_date_slider_function: function(PosActivationDropdown) {
            PosActivationScenarios = {'As planned (Dec 2021)':  0, 'Delayed 3 months (Mar 2022)': 1}
            if (PosActivationDropdown === 'Custom Value'){
                return window.dash_clientside.no_update
            }
            return PosActivationScenarios[PosActivationDropdown];
        },
        update_validator_adoption_slider_function: function(ValidatorDropdown) {
            ValidatorScenarios = {'Normal Adoption': 3, 'Low Adoption': 2, 'High Adoption':4};
            if (ValidatorDropdown === 'Custom Value'){
                return window.dash_clientside.no_update
            }
            return ValidatorScenarios[ValidatorDropdown];
        },
        update_mev_slider_function: function(EIP1559Dropdown) {
            EIP1559Scenarios = {'Disabled (MEV = 0)': 0, 'Enabled (MEV = 0.02)': 0.02}
            if (EIP1559Dropdown === 'Enabled (Custom Value)'){
                return window.dash_clientside.no_update
            }
            return EIP1559Scenarios[EIP1559Dropdown];
        },
        update_eth_supply_chart_function: function(EIP1559Slider, ValidatorAdoptionSlider, PosLaunchDate, FigurePlot) {
            LookUp = PosLaunchDate + ':' + EIP1559Slider + ':' + ValidatorAdoptionSlider
            HistoricalPlotData = FigurePlot[0]["historical"]["data"]
        
            if (FigurePlot[0][LookUp]["data"].length < 10){
                FigurePlot[0][LookUp]["data"] = HistoricalPlotData.concat(FigurePlot[0][LookUp]["data"])
            }
        
            if (ValidatorAdoptionSlider == 3){
                ValidatorDropdown = 'Normal Adoption'
            }
            else if (ValidatorAdoptionSlider == 2) {
                ValidatorDropdown = 'Low Adoption'
            }
            else if (ValidatorAdoptionSlider == 4) {
                ValidatorDropdown = 'High Adoption'
            }
            else{
                ValidatorDropdown = 'Custom Value'
            }
        
            if (EIP1559Slider == 0){
                EIP1559Dropdown = 'Disabled (Base Fee = 0)'
            }
            else if (EIP1559Slider == 30){
                EIP1559Dropdown = 'Enabled (Base Fee = 30)'
            }
            else {
                EIP1559Dropdown = 'Enabled (Custom Value)'
            }
            
            FigurePlotMobile = Object.assign({}, FigurePlot[0][LookUp]);
            FigurePlotMobile["layout"]["annotations"].length = 0
            FigurePlotMobile["data"] = FigurePlotMobile["data"].filter((obj) => obj.legendgroup !== "markers")

            FigurePlotDesktop = Object.assign({}, FigurePlot[0][LookUp]);
            return [FigurePlotDesktop, FigurePlotMobile, ValidatorDropdown, EIP1559Dropdown]
        }
    }
});
