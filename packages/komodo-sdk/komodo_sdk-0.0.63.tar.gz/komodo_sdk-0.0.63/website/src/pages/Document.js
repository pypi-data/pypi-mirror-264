import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import { BiMinus } from "react-icons/bi";
import menuIcon from "../assets/Frame.svg";
import Drawer from "react-modern-drawer";
import close from "../assets/close.svg";
import Header from "../components/Header";
import DocumentSidebar from "../components/document/DocumentSidebar";
import portfolio from '../../src/images/portfolio.png'
import docprofile from '../../src/images/docprofile.png'

const Document = () => {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen);
    };

    const [isDragging, setIsDragging] = useState(false);

    const handleDragStart = (event) => {
        event.dataTransfer.setData("text/plain", event.target.id);
        setIsDragging(true);
    };

    const handleDragEnd = () => {
        setIsDragging(false);
    };

    const handleDrop = (event) => {
        event.preventDefault();
        const draggableId = event.dataTransfer.getData("text/plain");
        const draggedElement = document.getElementById(draggableId);
        const dropTarget = event.currentTarget;

        if (dropTarget === event.target || dropTarget.contains(event.target)) {
            dropTarget.appendChild(draggedElement);
        }

        setIsDragging(false);
    };

    const handleDragOver = (event) => {
        event.preventDefault();
    };


    return (
        <>
            <div className="flex lg:block">
                <div className="z-[999]">
                    <img
                        src={menuIcon}
                        className={`hidden xl:flex xl:absolute w-[27px] h-[27px] mx-4 my-8 ${isDrawerOpen === true ? "xl:hidden" : ""
                            }`}
                        onClick={toggleDrawer}
                        alt=""
                    />
                </div>

                <div className="xl:hidden w-1/5 font-cerebri flex border-r-[0.5px] border-[#CDCDCD]">
                    <Sidebar />
                    <DocumentSidebar />
                </div>

                <Drawer
                    open={isDrawerOpen}
                    onClose={toggleDrawer}
                    direction="left"
                    className="chatDrawer"
                >
                    <Sidebar />
                    <div className="font-cerebri w-[-webkit-fill-available] flex flex-col justify-between">
                        <img
                            src={close}
                            className="w-[14px] h-[14px] absolute right-3 top-5"
                            onClick={toggleDrawer}
                            alt=""
                        />
                        <DocumentSidebar />
                    </div>
                </Drawer>

                <div className="w-full">
                    <Header />
                    <div className="flex lg:flex-col">
                        <div className="w-4/5 bg-[#f3f4f6] lg:w-full">
                            <div className="px-4 py-2">
                                <div className="bg-[#E0E8F8] rounded-md px-12 py-2 flex items-center justify-between">
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Agents</h1>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Risk Model Agent</h1>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">vs Benchmark Agent</h1>
                                    </div>
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Agent 3</h1>
                                </div>
                                <div className="bg-[#fff] rounded-xl px-12 py-3 mt-4 h-[calc(100vh-241px)]"
                                    id="drop-target"
                                    onDrop={handleDrop}
                                    onDragOver={handleDragOver}>
                                    <h1 className="text-[#3C3C3C] text-[18px] font-cerebri leading-[24px]">Canvas</h1>
                                </div>
                                <div className="bg-[#E0E8F8] rounded-md px-12 py-2 flex items-center justify-between mt-4">
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Audience</h1>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Risk Model Agent</h1>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <img src={docprofile} alt="docprofile" />
                                        <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">vs Benchmark Agent</h1>
                                    </div>
                                    <h1 className="text-[#3C3C3C] text-[14px] font-cerebriregular leading-[24px]">Agent 3</h1>
                                </div>
                            </div>
                        </div>
                        <div className="w-1/5 h-[calc(100vh-93px)] overflow-auto scrollbar border-l-[0.5px] border-[#CDCDCD] px-5 py-6  lg:w-full lg:h-auto">
                            <h1 className="text-[#3C3C3C] text-[20px] font-cerebri leading-[24px]">Outputs</h1>

                            <div className="mt-8 cursor-pointer"
                                id="drag-source"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}
                            >
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">Summary</p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">Concise</p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">Detailed</p>
                                </div>
                            </div>
                            <div className="mt-8 cursor-pointer"
                                id="drag-source1"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}>
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">Charts</p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">Most Relevant (Agent Chosen)</p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">User-annotated</p>
                                </div>
                            </div>

                            <h1 className="text-[#3C3C3C] text-[20px] font-cerebri leading-[24px] mt-6">Portfolio</h1>
                            <div className="mt-8 cursor-pointer"
                                id="drag-source2"
                                draggable
                                onDragStart={handleDragStart}
                                onDragEnd={handleDragEnd}>
                                <div className="flex items-center gap-3">
                                    <img src={portfolio} alt="portfolio" />
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px]">Tables</p>
                                </div>
                                <div className="mt-3 ms-20 xxl:ms-14">
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit">Most Relevant (Agent Chosen)</p>
                                    <p className="text-[#3C3C3C] text-[16px] font-cerebriregular leading-[24px] bg-customBg px-4 py-3 rounded-xl border border-customBorder w-fit mt-2">User-annotated</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Document;
