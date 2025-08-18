import $file.NutShell.build
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
