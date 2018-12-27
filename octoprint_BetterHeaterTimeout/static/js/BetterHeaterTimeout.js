$(function() {
    function BetterHeaterTimeoutViewModel(parameters) {
        var self = this;

		console.log("hi");

		self.onStartupComplete = () => console.log("HII!!!!!!!!!!!!!!!!");

		self.onEventFileSelected = () => console.log("THAR BE FILE SELECTAD");

		self.onDataUpdaterPluginMessage = (plugin, {event, payload}) => {
			console.log(plugin, event, payload)
			if(plugin !== "BetterHeaterTimeout") return;

			console.log("hi!", event, payload);

			if(event === "HeaterTimeout")
				return new PNotify({
					title: "HeaterTimeout",
					text: `Heater '${payload.heater}' disabled after ${payload.time_elapsed} seconds.`,
				});
		}
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: BetterHeaterTimeoutViewModel,
        dependencies: [],
        elements: []
    });
});
