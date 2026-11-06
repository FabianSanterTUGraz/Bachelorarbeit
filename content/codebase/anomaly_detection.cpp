#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "include/AnomalyDetection.h"

void writeData(const std::string& filePath, double* outX,
               double* outY, int fingerPrintSize, bool append = true)
{
    std::ofstream file;
    if (append)
    {
        file.open(filePath, std::ios_base::app);
    }
    else
    {
        file.open(filePath);
    }

    if (!file.is_open())
    {
        std::cerr << "Error: Could not open file at path: " << filePath << std::endl;
        return;
    }

    file.precision(15);
    file << "---NEW-FINGERPRINT-START---\n";
    for (int k = 0; k < fingerPrintSize; k++)
    {
        file << outX[k] << "," << outY[k] << '\n';
    }
    file.close();
}

int main(int argc, char* argv[])
{
    std::cout << "Real time anomaly detection...." << std::endl;
    if (argc < 4)
    {
        std::cerr << "Faulty usage pass parameter as followed: anomaly_detection <dimensions> <windowSize> <inputName>" << std::endl;
        return 1;
    }

    const int dimensions = std::stoi(argv[1]); // number of embedding dimensions
    const int windowSize = std::stoi(argv[2]); // length of the sliding window buffer
    std::string fileInput = argv[3];
    std::string absolutePath = "data/" + fileInput + ".csv";  //The data which will be plotted has to be in an Data folder in the same subdirectory as where the script is called.
    std::string line;

    int fingerPrintSize = windowSize - dimensions + 1;

    //
    double* slidingWindow       = new double[windowSize]();
    //
    double* tde                 = new double[dimensions]();
    //
    double* runningMean         = new double[dimensions]();
    //
    double* runningScatter      = new double[(size_t)dimensions * dimensions]();
    //
    double* principalComponent1 = new double[dimensions]();
    //
    double* principalComponent2 = new double[dimensions]();
    //
    double* outX                = new double[fingerPrintSize]();
    //
    double* outY                = new double[fingerPrintSize]();

    //
    principalComponent1[0] = 1.0;
    principalComponent2[1] = 1.0;

    std::string outputPath = "output/output.txt";
    bool append = false;

    std::ifstream dataStream(absolutePath);
    if(!dataStream.is_open())
    {
        std::cout << "Error could not open file!\n";
    }

    while (std::getline(dataStream,line))
    {
        double value = std::stod(line);

        if (updateStreamingPca(value, tde, slidingWindow, runningMean, runningScatter,principalComponent1,
                                principalComponent2, windowSize, dimensions,
                                outX, outY) == 0)
        {
            writeData(outputPath, outX, outY, fingerPrintSize, append);
            append = true;
        }
    }

    delete[] slidingWindow;
    delete[] tde;
    delete[] runningMean;
    delete[] runningScatter;
    delete[] principalComponent1;
    delete[] principalComponent2;
    delete[] outX;
    delete[] outY;
    return 0;
}