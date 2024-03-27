library(eadeploy)


move_to_webserver(
  "index.html",
  linkname = "pyeach",
  eid = Sys.info()[["user"]],
  overwrite = TRUE,
)