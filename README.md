# Airing Advisor

**Use indoor and outdoor temperature/humidity sensors to see when outside air is drier than the air indoors.**

The integration calculates absolute humidity for both locations and recommends airing out when indoor air has at least 1.0 g/m³ more water vapor than outdoor air. It creates a recommendation binary sensor and a humidity-difference sensor. This can help with moisture management when conditions outside are suitable.

## Install with HACS

1. In Home Assistant, open **HACS → Integrations**.
2. Open the **⋮** menu and choose **Custom repositories**.
3. Add `https://github.com/CodeArcade-ctrl/airing-advisor` and choose **Integration**.
4. Install **Airing Advisor**, then restart Home Assistant.
5. Open **Settings → Devices & services → Add integration**, search for **Airing Advisor**, and select indoor/outdoor temperature and humidity sensors.

Every user needs to add this custom repository in HACS. It is not yet included in the HACS default catalog.

## Entities

- **Ventilate recommended** turns on when outside air is at least 1.0 g/m³ drier than indoor air.
- **Indoor minus outdoor absolute humidity** shows the difference in g/m³; a positive value means indoor air contains more water vapor.

The recommendation refreshes every 60 seconds. Temperature sensors in °C or °F and relative-humidity sensors in percent are supported. No external API or account is used.

## Limitations

This is a moisture comparison, not an air-quality monitor. It cannot detect smoke, pollen, pollution, or weather conditions, and it does not guarantee that opening a window is appropriate. Consider other local conditions before acting on the recommendation.

## License

MIT. See [LICENSE](LICENSE).
