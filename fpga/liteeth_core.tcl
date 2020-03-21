prj_project new -name "liteeth_core" -impl "impl" -dev  -synthesis "synplify"
prj_src add "/home/niklas/colorlight/colorlight/framebuffer-udp/liteeth_core.v" -work work
prj_impl option top "liteeth_core"
prj_project save
prj_run Synthesis -impl impl -forceOne
prj_run Translate -impl impl
prj_run Map -impl impl
prj_run PAR -impl impl
prj_run Export -impl impl -task Bitgen