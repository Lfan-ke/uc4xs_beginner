package millbuild.NutShell

import _root_.mill.runner.MillBuildRootModule

@scala.annotation.nowarn
object MiscInfo_build {
  implicit lazy val millBuildRootModuleInfo: _root_.mill.runner.MillBuildRootModule.Info = _root_.mill.runner.MillBuildRootModule.Info(
    Vector("/home/heke/ysyx/uc4xs_newcomer/cache-ut/out/mill-launcher/0.11.13.jar").map(_root_.os.Path(_)),
    _root_.os.Path("/home/heke/ysyx/uc4xs_newcomer/cache-ut/NutShell"),
    _root_.os.Path("/home/heke/ysyx/uc4xs_newcomer/cache-ut"),
  )
  implicit lazy val millBaseModuleInfo: _root_.mill.main.RootModule.Info = _root_.mill.main.RootModule.Info(
    millBuildRootModuleInfo.projectRoot,
    _root_.mill.define.Discover[build]
  )
}
import MiscInfo_build.{millBuildRootModuleInfo, millBaseModuleInfo}
object build extends build
class build extends _root_.mill.main.RootModule.Foreign(Some(_root_.mill.define.Segments.labels("foreign-modules", "NutShell", "build"))) {

//MILL_ORIGINAL_FILE_PATH=/home/heke/ysyx/uc4xs_newcomer/cache-ut/NutShell/build.sc
//MILL_USER_CODE_START_MARKER
import mill._, scalalib._
import coursier.maven.MavenRepository

object ivys {
  val scala = "2.13.10"
  val chisel3 = ivy"edu.berkeley.cs::chisel3:3.5.6"
  val chisel3Plugin = ivy"edu.berkeley.cs:::chisel3-plugin:3.5.6"
}

trait CommonModule extends ScalaModule {
  override def scalaVersion = ivys.scala

  override def scalacOptions = Seq("-Ymacro-annotations") ++
    Seq("-Xfatal-warnings", "-feature", "-deprecation", "-language:reflectiveCalls")
}

trait HasChisel3 extends ScalaModule {
  override def repositoriesTask = T.task {
    super.repositoriesTask() ++ Seq(
      MavenRepository("https://oss.sonatype.org/content/repositories/snapshots")
    )
  }
  override def ivyDeps = Agg(ivys.chisel3)
  override def scalacPluginIvyDeps = Agg(ivys.chisel3Plugin)
}

trait HasChiselTests extends SbtModule {
  object test extends SbtModuleTests with TestModule.ScalaTest {
    override def ivyDeps = Agg(ivy"edu.berkeley.cs::chiseltest:0.5.4")
  }
}

trait CommonNS extends SbtModule with CommonModule with HasChisel3

object difftest extends CommonNS {
  override def millSourcePath = os.pwd / "difftest"
}

object chiselModule extends CommonNS with HasChiselTests {
  override def millSourcePath = os.pwd

  override def moduleDeps = super.moduleDeps ++ Seq(
    difftest
  )
}

}