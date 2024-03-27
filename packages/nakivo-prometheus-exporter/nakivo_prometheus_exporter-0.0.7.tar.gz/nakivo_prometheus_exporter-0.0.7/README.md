## Quick and dirty Nakivo Prometheus exporter

This tool connects to Navkio Backup & Replication API endpoint, and fetches licensing and backup state information in order to present this data as prometheus metrics.

## Quick start

Grab yourself a copy of `nakivo_prometheus_exporter` with
```
pip install nakivo_prometheus_exporter
```

Create your YAML config file in let's say `/etc/nakivo_prometheus_exporter.yaml`
```
http_server:
  listen: 0.0.0.0
  port: 9119
  username: me
  password: MySecret!Password
  # We usually don't authenticate for prometheus exporters
  no_auth: true
  log_file: /var/log/nakivo_prometheus_exporter.log
nakivo_hosts:
  - MyNakivoHost:
    host: https://mynakivohost.tld:4443
    username: readonly
    password: SomeNicePassword
    cert_verify: False
  - AnotherNakivoHost:
    host: https://othernakivo.local:4443
    username: readonly
    password: OtherPasswrod
    cert_verify: True
```

Once you're done, you can try to run the exporter with
```
nakivo_prometheus_exporter --config-file=/etc/nakivo_prometheus_eporter.yaml
```
Once running, you might want to check the metrics with:
```
curl http://localhost:9119/metrics
```

If everything works, you can use the provided systemd service file, copy it into `/etc/systemd/system` and run the service with
```
systemctl enable --now nakivo_prometheus_exporter
```

## Caveats

Since on every scraping, the exporter connects to *ALL* Nakivo API endpoints defined in the host section, you should set the scraper interval to something reasonable like 1 hour.

## Other caveats

This is a quick and dirty proof of concept, only fetching vm backup state and licensing state.  
There's still quiescing information missing (didn't find it in the (Nakivo API)[https://helpcenter.nakivo.com/api-reference/Content/API-Reference-Overview.htm])

There's also some need to add backup sizes and duration.  
Will be added if a bit of traction is observed.
