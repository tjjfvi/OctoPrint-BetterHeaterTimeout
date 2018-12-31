$(function() {
    function BetterHeaterTimeoutViewModel(parameters) {
        var self = this;

		self.onDataUpdaterPluginMessage = (plugin, { event, payload }) => {
			if(plugin !== "BetterHeaterTimeout") return;

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
