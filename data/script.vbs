If Not IsObject(application) Then
   Set SapGuiAuto  = GetObject("SAPGUI")
   Set application = SapGuiAuto.GetScriptingEngine
End If
If Not IsObject(connection) Then
   Set connection = application.Children(0)
End If
If Not IsObject(session) Then
   Set session    = connection.Children(0)
End If
If IsObject(WScript) Then
   WScript.ConnectObject session,     "on"
   WScript.ConnectObject application, "on"
End If
session.findById("wnd[0]").maximize
session.findById("wnd[0]/tbar[0]/okcd").text = "Y_RD0_49000090"
session.findById("wnd[0]").sendVKey 0
session.findById("wnd[0]/usr/ctxtSP$00006-LOW").text = ""
session.findById("wnd[0]/usr/ctxtSP$00008-LOW").text = ""
session.findById("wnd[0]/usr/ctxtSP$00006-LOW").setFocus
session.findById("wnd[0]/usr/ctxtSP$00006-LOW").caretPosition = 0
session.findById("wnd[0]/usr/btn%_SP$00004_%_APP_%-VALU_PUSH").press
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").text = "HU01"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").setFocus
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,1]").caretPosition = 4
session.findById("wnd[1]").sendVKey 0
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,2]").text = "CZ01"
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,2]").setFocus
session.findById("wnd[1]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/ctxtRSCSEL_255-SLOW_I[1,2]").caretPosition = 4
session.findById("wnd[1]").sendVKey 0
session.findById("wnd[1]/tbar[0]/btn[8]").press
session.findById("wnd[0]/usr/ctxtSP$00001-LOW").text = Day(Date())&"."&Month(Date())&"."&Year(Date())
session.findById("wnd[0]/usr/ctxtSP$00001-HIGH").text = Day(Date())&"."&Month(Date())&"."&Year(Date())
session.findById("wnd[0]/usr/ctxtSP$00003-LOW").text = "ZOR"
session.findById("wnd[0]/usr/ctxtSP$00003-HIGH").text = "ZOR"
session.findById("wnd[0]/usr/ctxtSP$00002-LOW").text = ""
session.findById("wnd[0]/usr/rad%DOWN").setFocus
session.findById("wnd[0]/usr/rad%DOWN").select
session.findById("wnd[0]/usr/txt%PATH").text = "C:\Users\Z0021338b\Documents\report.dat"
session.findById("wnd[0]/usr/txt%PATH").setFocus
session.findById("wnd[0]/usr/txt%PATH").caretPosition = 39
session.findById("wnd[0]/tbar[1]/btn[8]").press
session.findById("wnd[1]/usr/chkRSAQDOWN-COLUMN").selected = true
session.findById("wnd[1]/usr/chkRSAQDOWN-COLUMN").setFocus
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[1]/tbar[0]/btn[0]").press
session.findById("wnd[0]/tbar[0]/btn[3]").press
