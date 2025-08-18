package millbuild

import _root_.mill.runner.MillBuildRootModule

@scala.annotation.nowarn
object MiscInfo_build {
  implicit lazy val millBuildRootModuleInfo: _root_.mill.runner.MillBuildRootModule.Info = _root_.mill.runner.MillBuildRootModule.Info(
    Vector("/home/heke/ysyx/uc4xs_newcomer/cache-ut/out/mill-launcher/0.11.13.jar").map(_root_.os.Path(_)),
    _root_.os.Path("/home/heke/ysyx/uc4xs_newcomer/cache-ut"),
    _root_.os.Path("/home/heke/ysyx/uc4xs_newcomer/cache-ut"),
  )
  implicit lazy val millBaseModuleInfo: _root_.mill.main.RootModule.Info = _root_.mill.main.RootModule.Info(
    millBuildRootModuleInfo.projectRoot,
    _root_.mill.define.Discover[build]
  )
}
import MiscInfo_build.{millBuildRootModuleInfo, millBaseModuleInfo}
object build extends build
class build extends _root_.mill.main.RootModule {

//MILL_ORIGINAL_FILE_PATH=/home/heke/ysyx/uc4xs_newcomer/cache-ut/build.sc
//MILL_USER_CODE_START_MARKER
import millbuild.NutShell.build
import mill._, scalalib._
import coursier.maven.MavenRepository
import mill.scalalib.TestModule._

// 指定Nutshell的依赖
object difftest extends NutShell.build.CommonNS {
  override def millSourcePath = os.pwd / "NutShell" / "difftest"
}

// Nutshell 配置
object NtShell
    extends NutShell.build.CommonNS
    with NutShell.build.HasChiselTests {
  override def millSourcePath = os.pwd / "NutShell"
  override def moduleDeps = super.moduleDeps ++ Seq(
    difftest
  )
}

// UT环境配置
object ut extends NutShell.build.CommonNS with ScalaTest {
  override def millSourcePath = os.pwd
  override def moduleDeps = super.moduleDeps ++ Seq(
    NtShell
  )
}

}