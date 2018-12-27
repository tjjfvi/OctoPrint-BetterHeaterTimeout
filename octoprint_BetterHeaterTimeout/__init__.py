# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin

class BetterHeaterTimeoutPlugin(
	octoprint.plugin.SettingsPlugin,
    octoprint.plugin.TemplatePlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.printer.PrinterCallback,
):
	def initialize(self):
		self._printer.register_callback(self);
		self._temp_statuses = dict();

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False)]

	def get_assets(self):
		return dict(js=['js/BetterHeaterTimeout.js'])

	def on_printer_add_temperature(self, data):
		self._logger.info([self._temp_statuses, self._settings.get_float(["timeout"])])
		if not self._settings.get(["enabled"]) or not self._printer.is_ready():
			self._temp_statuses = dict();

		time = data["time"]

		for key in data:
			if key == "time":
				return

			if not data[key]["target"]:
				if key in self._temp_statuses:
					del self._temp_statuses[key]
			else:
				if key in self._temp_statuses:
					time_elapsed = time - self._temp_statuses[key]["start"]
					timeout = self._settings.get_float(["timeout"])
					if time_elapsed >= timeout:
						self._printer.set_temperature(key, 0);
						payload = dict(
							heater=key,
							time_elapsed=time_elapsed,
							timeout=timeout,
						)
						self._event_bus.fire("HeaterTimeout", payload)
						self._plugin_manager.send_plugin_message(self._identifier, dict(event="HeaterTimeout", payload=payload))
				else:
					self._temp_statuses[key] = dict(
						start=time
					)


	def get_settings_defaults(self):
		return dict(
			timeout=600,
			enabled=True
		)

	def get_update_information(self):
		return dict(
			BetterHeaterTimeout=dict(
				displayName="BetterHeaterTimeout",
				displayVersion=self._plugin_version,

				type="github_release",
				user="tjjfvi",
				repo="OctoPrint-BetterHeaterTimeout",
				current=self._plugin_version,

				pip="https://github.com/tjjfvi/OctoPrint-BetterHeaterTimeout/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "BetterHeaterTimeout"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = BetterHeaterTimeoutPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
