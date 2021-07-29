window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_eip1559_slider_function: function(EIP1559Dropdown) {
            EIP1559Scenarios = {'Disabled (Base Fee = 0)': 0, 'Enabled (Base Fee = 25)': 25, }
            if (EIP1559Dropdown === 'Enabled (Custom Value)'){
                return window.dash_clientside.no_update
            }
            console.log(EIP1559Dropdown)
            return EIP1559Scenarios[EIP1559Dropdown];
        },
        update_pos_date_slider_function: function(PosActivationDropdown) {
            PosActivationScenarios = {'As planned (Dec 2021)':  0, 'Delayed 3 months (Mar 2022)': 1, 'Delayed 6 months (Jun 2022)': 2}
            if (PosActivationDropdown === 'Custom Value'){
                return window.dash_clientside.no_update
            }
            return PosActivationScenarios[PosActivationDropdown];
        },
        update_validator_adoption_slider_function: function(ValidatorDropdown) {
            ValidatorScenarios = {'Normal Adoption': 3, 'Low Adoption': 1.5, 'High Adoption':4.5};
            if (ValidatorDropdown === 'Custom Value'){
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
                ValidatorDropdown = 'Custom Value'
            }
        
            if (EIP1559Slider == 0){
                EIP1559Dropdown = 'Disabled (Base Fee = 0)'
            }
            else if (EIP1559Slider == 25){
                EIP1559Dropdown = 'Enabled (Base Fee = 25)'
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
