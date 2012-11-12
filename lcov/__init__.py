import SCons

from SCons.Builder import Builder
from SCons.Script import Dir, Flatten, Mkdir

from os import path


class ToolLCovWarning(SCons.Warnings.Warning):
    pass


class LCovExecutableNotFound(ToolLCovWarning):
    pass


def lcov_generator(source, target, env, for_signature):
    cmd = ['lcov --capture']
    cmd += ['--output-file', target[0].abspath]

    if 'LCOVDIR' in env:
        cmd += ['--directory', str(Dir(env['LCOVDIR']))]

    return ' '.join(Flatten(cmd))


def lcov_emitter(source, target, env):
    return (target, source)


_lcov_builder = Builder(generator=lcov_generator,
                        emitter=lcov_emitter)


def generate(env):
    env['LCov'] = _detect(env)
    env['BUILDERS']['LCov'] = _lcov_builder

def _detect(env):
    try:
        return env['LCov']
    except KeyError:
        pass

    lcov = env.WhereIs('lcov')
    if lcov:
        return lcov

    raise SCons.Errors.StopError(LCovExecutableNotFound,
                                 'Cound not detect lcov executable')

    return None


def exists(env):
    return _detect(env)