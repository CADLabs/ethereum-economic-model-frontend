window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_eip1559_slider_function: function(EIP1559Dropdown) {
            EIP1559Scenarios = {'Disabled': 0, 'EnabledNoMEV': 100, 'EnabledMEV':70};
            if (EIP1559Dropdown === 'Custom'){
                return window.dash_clientside.no_update
            }
            return EIP1559Scenarios[EIP1559Dropdown];
        },
        update_validator_adoption_slider_function: function(ValidatorDropdown) {
            ValidatorScenarios = {'Normal Adoption': 3, 'Low Adoption': 1.5, 'High Adoption':4.5};
            if (ValidatorDropdown === 'Custom'){
                return window.dash_clientside.no_update
            }
            return ValidatorScenarios[ValidatorDropdown];
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
            else if (ValidatorAdoptionSlider == 1.5) {
                ValidatorDropdown = 'Low Adoption'
            }
            else if (ValidatorAdoptionSlider == 4.5) {
                ValidatorDropdown = 'High Adoption'
            }
            else{
                ValidatorDropdown = 'Custom'
            }
        
            if (EIP1559Slider == 0){
                EIP1559Dropdown = 'Disabled'
            }
            else if (EIP1559Slider == 70){
                EIP1559Dropdown = 'EnabledMEV'
            }
            else if (EIP1559Slider == 100){
                EIP1559Dropdown = 'EnabledNoMEV'
            }
            else {
                EIP1559Dropdown = 'Custom'
            }
            
            return [FigurePlot[0][LookUp], ValidatorDropdown, EIP1559Dropdown]
        }
    }
});
