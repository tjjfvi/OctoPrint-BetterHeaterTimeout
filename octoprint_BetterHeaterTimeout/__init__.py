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

	def on_printer_add_temperature(self, data):
		if not self._settings.get(["enabled"]) or not self._printer.is_ready():
			self._temp_statuses = dict();

		time = data["time"]

		for key in data:
			if key == "time":
				continue

			target = data[key]["target"]

			if not target:
				if key in self._temp_statuses:
					del self._temp_statuses[key]
			else:
				if key in self._temp_statuses:
					if self._settings.get(["since_change"]) and target != self._temp_statuses[key]["temp"]:
						self._temp_statuses[key] = dict(
							start=time,
							temp=target,
						)
					else:
						time_elapsed = time - self._temp_statuses[key]["start"]
						timeout = self._settings.get_float(["bedTimeout" if key == "bed" else "timeout"])
						if time_elapsed >= timeout:
							def send_gcode_lines(setting_name):
								self._printer.commands(self._settings.get([setting_name]) \
									.replace("$heater", key) \
									.replace("$time_elapsed", str(time_elapsed)) \
									.replace("$timeout", str(timeout)) \
									.split("\n"))

							send_gcode_lines("before_gcode");
							self._printer.set_temperature(key, 0);
							payload = dict(
								heater=key,
								time_elapsed=time_elapsed,
								timeout=timeout,
							)
							self._event_bus.fire("HeaterTimeout", payload)
							self._plugin_manager.send_plugin_message(self._identifier, dict(event="HeaterTimeout", payload=payload))
							send_gcode_lines("after_gcode");
				else:
					self._temp_statuses[key] = dict(
						start=time,
						temp=target,
					)

	def get_template_configs(self):
		return [dict(type="settings", custom_bindings=False)]

	def get_assets(self):
		return dict(js=['js/BetterHeaterTimeout.js'])

	def get_settings_defaults(self):
		return dict(
			bedTimeout=600,
			timeout=600,
			enabled=True,
			since_change=True,
			before_gcode='',
			after_gcode='M117 $heater timed out',
		)

	def get_settings_version(self):
		return 2

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
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = BetterHeaterTimeoutPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
