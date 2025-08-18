package ut_nutshell

import chisel3._
import chisel3.util._
import nutcore._
import top._
import chisel3.stage._

object CacheMain extends App {
  (new ChiselStage).execute(
    args,
    Seq(
      ChiselGeneratorAnnotation(() =>
        new Cache()(CacheConfig(ro = false, name = "tcache", userBits = 16))
      )
    )
  )
}
