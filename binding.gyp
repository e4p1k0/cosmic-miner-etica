{
  'conditions': [
    [ 'OS=="win"',
      {'variables': {'obj': 'obj'}},
      {'variables': {'obj': 'o'}}
    ]
  ],

  "targets": [
    {
      "target_name": "hybridminer",
      "sources": [
        "cpp/hybridminer/addon.cc",
        "cpp/hybridminer/hybridminer.cpp",
        "cpp/hybridminer/cpusolver.cpp",
        "cpp/hybridminer/sha3.c",
        "cpp/hybridminer/cudasolver.cpp",
        "cpp/hybridminer/cuda_sha3.cu"
      ],
      'cflags_cc+': [ '-O3', '-std=c++11' ],

      "include_dirs": ["<!(node -e \"require('nan')\")"],

      'rules': [{
        'extension': 'cu',
        'inputs': ['<(RULE_INPUT_PATH)'],
        'outputs':['<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).o'],
        'conditions': [
          [ 'OS=="win"',
            {'rule_name': 'cuda on windows',
             'message': "compile cuda file on windows",
             'process_outputs_as_sources': 1,
             'action': ['nvcc -c <(_inputs) -o <(_outputs)\
                        -cudart static -m64 -lineinfo -use_fast_math -O3 --keep --resource-usage -src-in-ptx  -Xptxas "-v --opt-level 3 --sp-bounds-check --warn-on-spills --warn-on-local-memory-usage --dont-merge-basicblocks" ',
                        '-gencode=arch=compute_60,code=\\\"sm_60,compute_60\\\"',
                        '-gencode=arch=compute_61,code=\\\"sm_61,compute_61\\\"',
                        '-gencode=arch=compute_70,code=\\\"sm_70,compute_70\\\"',
                        '-gencode=arch=compute_75,code=\\\"sm_75,compute_75\\\"',
                        '-gencode=arch=compute_80,code=\\\"sm_80,compute_80\\\"',
                        '-gencode=arch=compute_86,code=\\\"sm_86,compute_86\\\"'] 
            },
            {'rule_name': 'cuda on linux',
             'message': "compile cuda file on linux",
             'process_outputs_as_sources': 1,
             'action': ['nvcc','-std=c++11','-m64','-Xcompiler=\"-fpic\"',
                        '-c','<@(_inputs)','-o','<@(_outputs)',
                        '-gencode=arch=compute_60,code=\"sm_60,compute_60\"',
                        '-gencode=arch=compute_61,code=\"sm_61,compute_61\"',
                        '-gencode=arch=compute_70,code=\"sm_70,compute_70\"',
                        '-gencode=arch=compute_75,code=\"sm_75,compute_75\"',
                        '-gencode=arch=compute_80,code=\"sm_80,compute_80\"',
                        '-gencode=arch=compute_86,code=\"sm_86,compute_86\"']
            }
          ]
        ]
      }],

      'conditions': [
        [ 'OS=="mac"', {
          'libraries': ['-framework CUDA'],
          'include_dirs': ['/usr/local/include'],
          'library_dirs': ['/usr/local/lib'],
        }],
        [ 'OS=="linux"', {
          'libraries': ['-lcudart_static'],
          'include_dirs': ['/usr/local/include'],
          'library_dirs': ['/usr/local/lib',
                           '/usr/local/cuda/lib64'
                          ],
        }],
        [ 'OS=="win"', {
          'conditions': [
            ['target_arch=="x64"',
             { 'variables': { 'arch': 'x64' }},
             { 'variables': { 'arch': 'Win32' }}
            ],
          ],
          'variables': {
            'cuda_root%': '$(CUDA_PATH)'
          },

          'libraries': [
            'cudart_static.lib',
            'cuda_sha3.o'
          ],

          'library_dirs': [
            '<(cuda_root)/lib/<(arch)',
            '<(module_root_dir)/build/Release/obj/hybridminer'
          ],

          "include_dirs": [
            "<(cuda_root)/include",
            'cpp/hybridminer'
          ]
        }]
      ],
      'configurations': {
        'Release': {
          'msvs_settings': {
            'VCCLCompilerTool': {
              'SuppressStartupBanner': 'true',
# Next line controls CPU ISA optimizations: 0=default, 1=SSE, 2=SSE2, 3=AVX, 4=none, 5=AVX2
#              'EnableEnhancedInstructionSet': 5,
              'FavorSizeOrSpeed': 1,
              'InlineFunctionExpansion': 2,
              'MultiProcessorCompilation': 'true',
              'Optimization': 3,
              'RuntimeLibrary': 0,
              'WarningLevel': 3,
              'ExceptionHandling': 1,
              'DebugInformationFormat': 3,
              'AdditionalIncludeDirectories': [ '..\\cpp\\hybridminer' ]
            }
          }
        }
      },
    }
  ]
}
