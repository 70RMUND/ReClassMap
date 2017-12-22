from ReClassMap import *

OFFSET_CLIENTGAMECONTEXT 	= 0x1437a8f48
OFFSET_DX11RENDERER 		= 0x143998828

r = Map("./BF1.reclass")

C = r.Class(name="OFFSET_ClientGameContext",offset=OFFSET_CLIENTGAMECONTEXT)
C[0x0000] = Pointer(classname="ClientGameContext", name="p_ClientGameContext")

C = r.Class(name="ClientGameContext",size=0x0440)
C[0x0010] = Int64(name="m_messageManager")
C[0x0020] = Pointer(classname="ClientPlayerManager",name="m_pClientPlayerManager_0")  
C[0x0028] = Pointer(classname="GameTime",name="m_pGameTime") 
C[0x0030] = Pointer(classname="Level",name="m_pLevel") 
C[0x0068] = Pointer(classname="ClientPlayerManager",name="m_pClientPlayerManager_1") 
C[0x0070] = Pointer(classname="OnlineManager",name="m_pOnlineManager") 
C[0x0078] = Pointer(classname="GameView",name="m_pGameView") 

C = r.Class(name="ClientPlayerManager",size=0x0840)
C[0x0008] = Pointer(classname="PlayerData",name="m_pPlayerData")
C[0x0550] = Pointer(classname="ClientPlayer",name="*m_ppPlayers_0") 
C[0x0570] = Pointer(classname="ClientPlayer",name="*m_ppPlayers_1 ") 
C[0x0578] = Pointer(classname="ClientPlayer",name="m_pLocalPlayer")

C = r.Class(name="OFFSET_DXRenderer",offset=OFFSET_DX11RENDERER)
C[0x0000] = Pointer(classname="DXRenderer", name="p_DXRenderer")

C = r.Class(name="DXRenderer")
C[0x0810] = Int32(name="m_frameCounter")
C[0x0814] = Int32(name="m_framesInProgress")
C[0x0818] = Int32(name="m_framesInProgress2")
C[0x081C] = Byte(name="m_isActive")
C[0x0820] = Pointer(classname="Screen",name="m_pScreen")  
C[0x0868] = Pointer(classname="DXDisplaySettings",name="m_pDx11DisplaySettings")
C[0x08A0] = Pointer(classname="ID3D11Device",name="m_pDevice") 
C[0x08A8] = Pointer(classname="ID3D11DeviceContext",name="m_pContext") 
C[0x0918] = Pchar(name="m_AdapterName")


r.write(hidepad=1,custompad=1)