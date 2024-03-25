import os.path
from jinja2 import Environment, FileSystemLoader

from steam_sdk.parsers import templates
from steam_sdk.data.DataModelParsimDakota import DataModelParsimDakota
from steam_sdk.data.DataDakota import DataDakota
from steam_sdk.data.DataSettings import DataSettings
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing

class ParserDakota:

    @staticmethod
    def assemble_in_file(
            data_model_dakota: DataModelParsimDakota,
            settings: DataSettings,
            dakota_in_folder_path: str = None,
            output_file_name = None
            ):
        """
        Generates Dakota compatible input file (with the .in extension) from TEAM SDK Dakota yaml file. It uses the template file of .in file.
        :param data_model_dakota: data class of data model dakota
        :type data_model_dakota: List[str]
        :param settings: settings object
        :type settings: DataSettings
        :param dakota_in_folder_path: optional output path (mostly used for testing)
        :param output_file_name: allows changing output file name (mostly used for testing)
        :type output_file_name: str
        :type dakota_in_folder_path: str
        :return: Writes .in file to disk
        :rtype: None
        """

        # prepare dakota data for easier looping in the template
        dd = DataDakota()
        for name, var in data_model_dakota.study.variables.items():
            if data_model_dakota.study.type == 'multidim_parameter_study':
                dd.partitions.append(var.data_points - 1)
            elif data_model_dakota.study.type == 'optpp_q_newton':
                dd.initial_point.append(var.initial_point)
                #dd.descriptors.append(var.descriptors)
            dd.lower_bounds.append(var.bounds.min)
            dd.upper_bounds.append(var.bounds.max)

        # load template
        loader = FileSystemLoader(templates.__path__)
        env = Environment(loader=loader, variable_start_string='<<', variable_end_string='>>',
                          trim_blocks=True, lstrip_blocks=True)
        env.globals.update(len=len)
        template = 'template_Dakota.in'
        in_template = env.get_template(template)

        # propagate data in the template
        output_from_parsed_template = in_template.render(dmd=data_model_dakota, dd=dd)

        # prepare output folder and file path
        if not dakota_in_folder_path:
            dakota_in_folder_path = os.path.join(settings.local_Dakota_folder, data_model_dakota.parsim_name)
        make_folder_if_not_existing(dakota_in_folder_path)
        if not output_file_name:
            output_file_name = "dakota_in.in"
        dakota_in_output_file_path = os.path.join(dakota_in_folder_path, output_file_name)

        # save output file in the dakota_in_output_folder_path
        with open(dakota_in_output_file_path, "w") as tf:
            tf.write(output_from_parsed_template)
